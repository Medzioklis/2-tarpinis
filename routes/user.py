from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from services.user_functions import top_up_balance
from services.order_services import get_cart_contents, add_product_to_cart, create_order_from_cart
from services.product_services import get_product_by_id
from services.order_services import update_cart_item_quantity, remove_item_from_cart
from models.cart_class import Cart, db
from sqlalchemy import select


user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/')
@login_required
def dashboard():
    if current_user.user_role != 2:
        flash("Neturite prieigos prie naudotojo puslapio.", "danger")
        return redirect(url_for('auth.login'))
    return render_template('user/dashboard.html', user=current_user)



@user_bp.route('/add_balance', methods = ['GET','POST'])
@login_required
def add_balance():
    return top_up_balance()

@user_bp.route('/cart')
@login_required
def cart():
    try:
        cart_items, total = get_cart_contents(current_user.id)
        return render_template('user/cart.html', title='Krepšelis', cart_items=cart_items, total=total)
    except Exception as e:
        flash(f"Klaida gaunant krepšelio turinį: {e}", "danger")
        return render_template('user/cart.html', title='Krepšelis', cart_items=[], total=0)

@user_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = get_product_by_id(product_id)
    if product and product.stock > 0:
        try:
            add_product_to_cart(current_user.id, product_id)
            flash(f'Prekė "{product.name}" pridėta į krepšelį.', 'success')
        except Exception as e:
            flash(f'Nepavyko pridėti prekės: {e}', 'danger')
    elif not product:
        flash('Prekė nerasta.', 'danger')
    else:
        flash(f'Atsiprašome, prekės "{product.name}" laikinai neturime.', 'warning')
    return redirect(url_for('home.products'))

@user_bp.route('/buy_cart', methods=['POST'])
@login_required
def buy_cart():
    try:
        order = create_order_from_cart(current_user.id)
        flash(f'Ačiū, kad pirkote! Jūsų užsakymo Nr. {order.id}.', 'success')
        return redirect(url_for('home.index'))
    except ValueError as e:
        flash(str(e), 'danger')
        return redirect(url_for('user.cart'))
    except Exception as e:
        flash(f'Įvyko nenumatyta pirkimo klaida: {e}', 'danger')
        return redirect(url_for('user.cart'))
    
@user_bp.route('/cart/update/product_id>', methods=['POST'])
@login_required
def update_quantity(product_id):
    try:
        quantity = int(request.form.get('quantity'))
        if quantity < 1:
            flash("Kiekis turi būti bent 1.", "warning")
        else:
            update_cart_item_quantity(current_user.id, product_id, quantity)
            flash("Prekės kiekis atnaujintas.", "success")
    except ValueError as e:
        flash(str(e), "danger")
    except Exception as e:
        flash(f"Klaida atnaujinant kiekį: {e}", "danger")
    return redirect(url_for('user.cart'))

@user_bp.route('/cart/remove/<product_id>', methods=['POST'])
@login_required
def remove_item(product_id):
    try:
        remove_item_from_cart(current_user.id, product_id)
        flash("Prekė pašalinta iš krepšelio.", "info")
    except Exception as e:
        flash(f"Klaida šalinant prekę: {e}", "danger")
    return redirect(url_for('user.cart'))


@user_bp.route('/buy_cart_success', methods=['POST'])
@login_required
def buy_cart_success():
    from sqlalchemy import select
    stmt = select(Cart).where(Cart.user_id == current_user.id) # 1. Išrenkame visas krepšelio prekes naudotojui
    cart_items = db.session.scalars(stmt).all()

    if not cart_items:# 2. Jei krepšelis tuščias – rodomas pranešimas ir grąžinama atgal į krepšelį
        flash("Krepšelis tuščias.", "danger")
        return redirect(url_for("user.cart"))
    
    total = sum(item.product.price * item.quantity for item in cart_items) # 3. Apskaičiuojama bendra pirkinių suma

    if current_user.user_balance < total:     # 4. Jei naudotojo balansas per mažas – rodomas pranešimas ir grąžinama atgal
        flash("Nepakanka lėšų.", "danger")
        return redirect(url_for("user.cart"))
  
    current_user.user_balance -= total # 5. Nuskaitome naudotojo balansą

    for item in cart_items: # 6. Pašaliname visas prekes iš krepšelio (tarsi jas "nupirkome")
        db.session.delete(item)

    db.session.commit()

    flash("Prekės sėkmingai įsigytos!", "success")
    return render_template("store/purchase_success.html", user=current_user, items=cart_items)




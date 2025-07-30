from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from services.user_functions import top_up_balance
from services.order_services import get_cart_contents, add_product_to_cart
from services.product_services import get_product_by_id


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



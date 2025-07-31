from flask import Blueprint, render_template, redirect, url_for, flash 
from forms.user_crud_form import  db 
from forms.product_form import AddProductForm, UpdateProductForm
from models.product_class import Product
from flask_login import login_required, current_user
from services.product_services import view_products
from models.review_class import Review
from forms.review_form import ReviewForm
from sqlalchemy import select

product_bp = Blueprint('product', __name__, template_folder='templates')

@product_bp.route('/admin_products')
def list_products():
    products = view_products()
    return render_template('admin/admin_products.html', products=products)

# Funkcija skirta pridėti prekę
@product_bp.route('/products/add', methods=['GET', 'POST'])
def add_product():
    # Sukuriamas formos objektas
    form = AddProductForm()
    # Tikrinama ar forma buvo pateikta (POST) ir ar duomenys joje yra galiojantys
    if form.validate_on_submit(): # Patikrina formą ir ar viskas suvesta tvarkingai
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data
            )
        db.session.add(product)
        db.session.commit()
        flash('Prekė sėkmingai pridėta.', 'success')
        return redirect(url_for('product.list_products'))
    return render_template('admin/add_product.html', form=form)

#  Funkcija, kuri leidžia redaguoti prekę

@product_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    # Bandoma gauti prekę iš duomenų bazės pagal ID
    product = db.session.get(Product, product_id)
    # Tikrina ar prekės nėra nerasta arba pažymėta kaip neaktyvi (ištrinta)
    if not product:
        flash('Prekė nerasta.', 'danger')
        return redirect(url_for('product.list_products'))

    form = UpdateProductForm(obj=product) # paima reiksmes kurios yra
    # Tikrinama ar forma buvo pateikta ir ar visi laukai galiojantys (praėjo validaciją)
    if form.validate_on_submit(): # Patikrina formą ir ar viskas suvesta tvarkingai
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        if form.is_active.data == '1':
            product.is_active = True
        else:
            product.is_active = False
        db.session.commit()
        flash('Prekė atnaujinta.', 'success')
        return redirect(url_for('product.list_products'))

    return render_template('admin/update_product.html', form=form, product=product, title="Redaguoti prekę")

# Funkcija leidžianti ištrinti prekę
@product_bp.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = db.session.get(Product, product_id) # Bandoma gauti prekę iš duomenų bazės pagal ID
    # Tikrinama ar prekė neegzistuoja arba jau yra neaktyvi (t. y. ištrinta)
    if not product: # Tikrinama ar prekė neegzistuoja arba jau yra neaktyvi (gal jau ištrinta)
        flash('Prekė nerasta arba jau ištrinta.', 'warning')
    else:
        product.deleted = True # product lenetei deleted True
        db.session.commit()
        flash('Prekė pašalinta iš prekybos.', 'warning')
    return redirect(url_for('product.list_products'))

#  Atsiliepimų peržiūra
@product_bp.route('/product/<int:product_id>/review')
def product_review(product_id):
    stmt = select(Product).where(Product.id == product_id)
    product = db.session.execute(stmt).scalar_one_or_none()

    if not product:
        flash('Prekė nerasta', 'warning')
        return redirect(url_for('product.list_products')) 

    return render_template('product_review.html', product=product)


# Pridėti prekės įvertinimą
@product_bp.route('/products/<int:product_id>/review', methods=['GET', 'POST'])
@login_required
def leave_review(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        flash("Prekė nerasta", "danger")
        return redirect(url_for('product.list_products'))

    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            rating=form.rating.data,
            comment=form.comment.data,
            user_id=current_user.id,
            product_id=product.id
        )
        db.session.add(review)
        db.session.commit()
        flash("Atsiliepimas pateiktas!", "success")
        return redirect(url_for('product.product_review', product_id=product.id))

    return render_template('products/leave_review.html', form=form, product=product)



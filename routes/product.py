from flask import Blueprint, render_template, redirect, url_for, flash
from forms.user_crud_form import  db 
from forms.product_form import AddProductForm
from models.product import Product

product_bp = Blueprint('product', __name__, template_folder='templates')

@product_bp.route('/products')
def view_products():
    return render_template('products/view_all')

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
        return redirect(url_for('product.view_products'))
    return render_template('add_product.html', form=form)

#  Funkcija, kuri leidžia redaguoti prekę

@product_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    # Bandoma gauti prekę iš duomenų bazės pagal ID
    product = db.session.get(Product, product_id)
    # Tikrina ar prekės nėra nerasta arba pažymėta kaip neaktyvi (ištrinta)
    if not product or not product.is_active:
        flash('Prekė nerasta.', 'danger')
        return redirect(url_for('product.view_products'))

    form = AddProductForm(obj=product)
    # Tikrinama ar forma buvo pateikta ir ar visi laukai galiojantys (praėjo validaciją)
    if form.validate_on_submit(): # Patikrina formą ir ar viskas suvesta tvarkingai
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        db.session.commit()
        flash('Prekė atnaujinta.', 'success')
        return redirect(url_for('product.view_products'))

    return render_template('edit_product.html', form=form, product=product)

# Funkcija leidžianti ištrinti prekę
@product_bp.route('/products/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = db.session.get(Product, product_id) # Bandoma gauti prekę iš duomenų bazės pagal ID
    # Tikrinama ar prekė neegzistuoja arba jau yra neaktyvi (t. y. ištrinta)
    if not product or not product.is_active: # Tikrinama ar prekė neegzistuoja arba jau yra neaktyvi (gal jau ištrinta)
        flash('Prekė nerasta arba jau ištrinta.', 'warning')
    else:
        product.is_active = False # Priešingu atveju, nustatoma, kad prekė nebėra aktyvi (soft delete)
        db.session.commit()
        flash('Prekė pašalinta iš prekybos.', 'warning')
    return redirect(url_for('product.view_products'))

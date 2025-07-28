from flask import Blueprint, render_template, redirect, url_for, flash
from models.product import Product
from forms.product_form import ProductForm
from database import db

products_bp = Blueprint('products', __name__)

@products_bp.route('/add-product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            quantity=form.quantity.data,
            stock_left=form.stock_left.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Prekė sėkmingai pridėta!', 'success')
        return redirect(url_for('products.add_product'))
    return render_template('add_product.html', form=form)
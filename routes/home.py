from flask import Blueprint, redirect, url_for, render_template, flash, request
from forms.review_form import ReviewForm
from flask_login import current_user
from services.product_services import add_review_to_product, get_product_by_id, get_all_products

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    return render_template('index.html')

@home_bp.route('/product/<product_id>', methods = ['GET','POST'])
def product_detail(product_id):
    product = get_product_by_id(product_id)
    if not product:
        flash("Prekė nerasta.", "danger")
        return redirect(url_for('home.products'))

    form = ReviewForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        try:
            add_review_to_product(
                product_id=product.id,
                user_id=current_user.id,
                rating=form.rating.data,
                text=form.text.data
            )
            flash('Ačiū už jūsų atsiliepimą!', 'success')
            return redirect(url_for('home.product_detail', product_id=product.id))
        except Exception as e:
            flash(f"Klaida pateikiant atsiliepimą: {e}", "danger")

    return render_template('store/product_detail.html', title=product.name, product=product, form=form)

@home_bp.route('/products')
def products():
    sort_by = request.args.get('sort_by', 'price_asc')
    try:
        all_products = get_all_products(sort_by=sort_by)
        return render_template('store/products.html', title='Prekės', products=all_products)
    except Exception as e:
        flash(f"Klaida gaunant prekes: {e}", "danger")
        return render_template('store/products.html', title='Prekės', products=[])

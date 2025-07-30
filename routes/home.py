from flask import Blueprint, render_template, request, flash
from services.product_services import get_all_products

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    return render_template('index.html')

@home_bp.route('/products')
def products():
    sort_by = request.args.get('sort_by', 'price_asc')
    try:
        all_products = get_all_products(sort_by=sort_by)
        return render_template('store/products.html', title='Prekės', products=all_products)
    except Exception as e:
        flash(f"Klaida gaunant prekes: {e}", "danger")
        return render_template('store/products.html', title='Prekės', products=[])
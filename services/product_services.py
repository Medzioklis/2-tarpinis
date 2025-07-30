from flask import Blueprint, render_template, redirect, url_for, flash, request
from sqlalchemy import select
from database import db
from forms.product_form import AddProductForm
from models.product import Product


# Funkcija leidžianti peržiūrėti visas prekes
def view_products():
    products = db.session.execute(db.select(Product).where(Product.is_active == True)).scalars().all()
    return render_template('view_all.html', products=products)





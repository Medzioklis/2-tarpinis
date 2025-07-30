from flask import render_template
from database import db
from models.product_class import Product


# Funkcija leidžianti peržiūrėti visas prekes
def view_products():
    products = db.session.execute(db.select(Product).where(Product.deleted == False)).scalars().all()
    return products




from models.review_class import Review, db
from models.product_class import Product
from flask import flash
from sqlalchemy import select, desc, asc


# Funkcija leidžianti peržiūrėti visas prekes
def view_products():
    products = db.session.execute(db.select(Product).where(Product.deleted == False)).scalars().all()
    return products


def get_product_by_id(product_id):
    try:
        return Product.query.get(int(product_id))
    except (ValueError, TypeError):
        return None
    
def add_review_to_product(product_id, user_id, rating, text):
    try:
        review = Review(product_id=product_id, user_id=user_id, rating=rating, text=text)
        db.session.add(review)
        db.session.commit()
        return review
    except Exception as e:
        db.session.rollback()
        raise e
    
def get_all_products(sort_by='price_asc'):
    """ Gauna visas aktyvias prekes, surikiuotas pagal nurodytą kriterijų. """
    try:
        rows = select(Product).where(Product.is_active==True)
        if sort_by == 'price_desc':
            rows = rows.order_by(desc(Product.price))
        elif sort_by == 'name':
            rows = rows.order_by(asc(Product.name))
        else: # Default: price_asc
            rows = rows.order_by(asc(Product.price))

        products = db.session.scalars(rows).all()
        return products
    except Exception as e:
        # Reikėtų loginti klaidą
        flash(f"Error getting all products: {e}")
        return []

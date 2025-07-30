from database import db
from models.product_class import Product
from sqlalchemy import asc, desc, select


# Funkcija leidžianti peržiūrėti visas prekes
def view_products():
    products = db.session.execute(db.select(Product).where(Product.deleted == False)).scalars().all()
    return products

# Gaunam visas aktyvias prekes surikiuotas pagal nurodytą kriterijų
def get_all_products(sort_by='price_asc'):
    try:
        rows = select(Product).where(Product.is_active == True)
        if sort_by == 'price_desc':
            rows = rows.order_by(desc(Product.price))
        elif sort_by == 'name':
            rows = rows.order_by(asc(Product.name))
        else: # Numatytasis rikiavimas pagal kainą didėjimo tvarka
            rows = rows.order_by(asc(Product.price))

        products = db.session.scalars(rows).all()
        return products
    except Exception as e:
        print(f"Klaida gaunant produktus: {e}")
        return []

# Gaunam produktą pagal ID
def get_product_by_id(product_id):
    try:
        product = db.session.get(Product, int(product_id))
        return product
    except ValueError:
        return None
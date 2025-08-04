from sqlalchemy import func, select
from models.product_class import Product
from models.review_class import Review
from models.order_class import Order
from database import db

# Grąžina prekių sąrašą, surikiuotą pagal vidutinį įvertinimą
# Rezultatas: sąrašas eilučių su (prekės pavadinimas, vidutinis įvertinimas, atsiliepimų kiekis)
def get_best_rated_products():
    best_rated_query = (
        select(
            Product.name,
            func.avg(Review.rating).label('vidutinis_ivertinimas'),
            func.count(Review.id).label('atsiliepimu_kiekis')
        )
        .join(Review, Product.reviews)  # Galima naudoti ryšį tiesiogiai
        .group_by(Product.id)
        .order_by(
            func.avg(Review.rating).desc(),
            func.count(Review.id).desc()
        )
        .limit(10) # Pasirenkame pvz., Top 10 prekių
    )
    
    best_rated_products = db.session.execute(best_rated_query).all()
    return best_rated_products
        
# Menesiu statistika
def get_monthly_profits():
    monthly_profit_query = (
        select(
            func.extract('year', Order.timestamp).label('metai'),
            func.extract('month', Order.timestamp).label('menuo'),
            func.sum(Order.total_price).label('menesio_apyvarta')
        )
        .where(Order.deleted == False) 
        .group_by('metai', 'menuo')
        .order_by(func.sum(Order.total_price).desc())
    )
    monthly_profits = db.session.execute(monthly_profit_query).all()
    return monthly_profits
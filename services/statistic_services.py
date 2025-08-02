from sqlalchemy import func, select
from .models import Order, OrderItem, Product, Review
from database import db


#     Grąžina statistiką apie pardavimus kiekvienai dienai
#     Rezultatas: sąrašas eilučių su (diena, parduotų prekių kiekis, dienos apyvarta)
def get_daily_sales_stats():

    daily_stats_query = (
        select(
            func.date(Order.timestamp).label('diena'),
            func.sum(OrderItem.quantity).label('parduotu_prekiu_kiekis'),
            func.sum(OrderItem.quantity * OrderItem.price_per_unit).label('dienos_apyvarta')
        )
        .join(Order, OrderItem.order_id == Order.id)
        .group_by(func.date(Order.timestamp))
        .order_by(func.date(Order.timestamp).desc())
    )
    
    daily_stats = db.session.execute(daily_stats_query).all()
    
    # Pavyzdinis atvaizdavimas konsolėje
    for diena, kiekis, apyvarta in daily_stats:
        print(f"Data: {diena}, Parduota vnt.: {kiekis}, Apyvarta: {apyvarta:.2f} €")
        
    return daily_stats
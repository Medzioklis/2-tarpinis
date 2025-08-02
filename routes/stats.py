from flask import Blueprint, render_template, request
from sqlalchemy import func, select, extract
from models.order_class import Order, OrderItem
from models.product_class import Product
from database import db
from datetime import datetime

stats_bp = Blueprint('statistic', __name__)

@stats_bp.route('/stats')
def stats():
    # Gauname parametrus iš URL
    period = request.args.get('period')
    date_filter_str = request.args.get('date_filter')

    # Numatytosios reikšmės
    stats_data = []
    title = "Pasirinkite laikotarpį"
    header_label = "Laikotarpis"

    # Tikriname, ar pateikti abu filtrai (periodas ir data)
    if period and date_filter_str:
        try:
            # Bazinė užklausa
            query = select(
                func.sum(OrderItem.quantity).label('kiekis'),
                func.sum(OrderItem.quantity * OrderItem.price_per_unit).label('apyvarta')
            ).join(Order, OrderItem.order_id == Order.id).join(Product, OrderItem.product_id == Product.id)

            if period == 'day':
                selected_date = datetime.strptime(date_filter_str, '%Y-%m-%d').date()
                query = query.add_columns(Product.name.label('label')).where(func.date(Order.timestamp) == selected_date).group_by(Product.name)
                title = f"Statistika {selected_date.strftime('%Y-%m-%d')} dienai"
                header_label = "Prekė"

            elif period == 'month':
                year, month = map(int, date_filter_str.split('-'))
                query = query.add_columns(func.date(Order.timestamp).label('label')).where(
                    extract('year', Order.timestamp) == year,
                    extract('month', Order.timestamp) == month
                ).group_by(func.date(Order.timestamp)).order_by(func.date(Order.timestamp))
                title = f"Statistika {year}-{month:02d} mėnesiui"
                header_label = "Diena"

            elif period == 'year':
                year = int(date_filter_str)
                query = query.add_columns(extract('month', Order.timestamp).label('label')).where(
                    extract('year', Order.timestamp) == year
                ).group_by(extract('month', Order.timestamp)).order_by(extract('month', Order.timestamp))
                title = f"Statistika {year} metams"
                header_label = "Mėnuo"
            
            stats_data = db.session.execute(query).all()
            if not stats_data:
                title = f"Duomenų nerasta laikotarpiui: {date_filter_str}"

        except (ValueError, TypeError):
            title = "Neteisingas datos formatas. Pabandykite dar kartą."
    
    # Perduodame gautus parametrus atgal į šabloną, kad forma "atsimintų" pasirinkimus
    return render_template('statistic/stats.html', 
                           title=title, 
                           header_label=header_label, 
                           stats_data=stats_data,
                           selected_period=period,
                           date_filter_value=date_filter_str)


# Grąžinaм statistiką apie pelningiausius mėnesius
def get_monthly_profitability():
    monthly_profit_query = (
        select(
            func.extract('year', Order.timestamp).label('metai'),
            func.extract('month', Order.timestamp).label('menuo'),
            func.sum(Order.total_price).label('menesio_apyvarta')
        )
        .group_by('metai', 'menuo')
        .order_by(func.sum(Order.total_price).desc())
    )
    
    monthly_profits = db.session.execute(monthly_profit_query).all()
    return render_template('statistic/stats.html', m_stats=monthly_profits)
        
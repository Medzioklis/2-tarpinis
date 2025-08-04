from database import db
from sqlalchemy import func #laikas dabar

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=func.now())
    total_price = db.Column(db.Float, nullable=False)
    
    # backref yra SQLAlchemy magija kuria jis pats atmintyje sukuria Order modelyje customer, skiriasi nuo back_populates tuo kad nebutina kode apsirasyt customer
    items = db.relationship('OrderItem', backref='order')

    def __repr__(self):
        return f'<Order {self.id}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<OrderItem Order:{self.order_id} Product:{self.product_id}>'
from database import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, default=True, nullable=False) # Išėmimui iš prekybos

    reviews = db.relationship("Review", backref='product')

    # backref yra SQLAlchemy magija kuria jis pats atmintyje sukuria Order modelyje customer, skiriasi nuo back_populates tuo kad nebutina kode apsirasyt customer
    order_items = db.relationship('OrderItem', backref="product")

    @property
    def average_rating(self):
        if not self.reviews:
            return 0
        total = sum(review.rating for review in self.reviews)
        return round(total / len(self.reviews), 1)
    
    
    def __repr__(self):
        return f'<Product {self.name}>'
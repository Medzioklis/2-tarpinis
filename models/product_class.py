from database import db

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, default=True, nullable=False) # Išėmimui iš prekybos

    # Produktas gali būti daugelyje krepšelio įrašų
    cart_items = db.relationship('Cart', back_populates='product')


    def __repr__(self):
        return f'<Product {self.name}>'
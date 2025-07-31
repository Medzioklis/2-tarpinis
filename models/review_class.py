
from sqlalchemy import ForeignKey
from database import db

class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey('products.id'), nullable=False)
    
    user = db.relationship('User', back_populates = 'reviews')
    product = db.relationship("Product", back_populates="reviews")
   

    def __repr__(self):
        return f'<Review {self.id}>'

from sqlalchemy import ForeignKey, func
from database import db
from datetime import datetime
import statistics


class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=func.now())
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey('products.id'), nullable=False)
    
    user = db.relationship('User', back_populates = 'reviews')
    product = db.relationship("Product", back_populates="reviews")
   
    # apskaičiuojam prekės įvertinimų vidurkį
    @property
    def average_rating(self):
        try:
            ratings = [review.rating for review in self.reviews]
            return round(statistics.mean(ratings), 1) if ratings else 0
        except statistics.StatisticsError:
            return 0

    def __repr__(self):
        return f'<Review {self.id}>'
from config import db


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(25), nullable=False)
    user_lastname = db.Column(db.String(25), nullable=False)
    user_email = db.Column(db.String(50), nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.Integer, default=2)


    def __str__(self):
        return f'Vartotojas: {self.user_name} {self.user_lastname}, paštas: {self.user_email}, slaptažodis: {self.user_password}'
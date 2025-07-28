from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    name = StringField('Pavadinimas', validators=[DataRequired()])
    description = StringField('Aprašymas')
    price = FloatField('Kaina', validators=[DataRequired()])
    quantity = IntegerField('Užsakytas kiekis', validators=[DataRequired()])
    stock_left = IntegerField('Sandėlio likutis', validators=[DataRequired()])
    submit = SubmitField('Išsaugoti')
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, FloatField
from wtforms.validators import  DataRequired, Length, NumberRange


class AddProductForm(FlaskForm):
    name = StringField('Prekės pavadinimas', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Aprašymas')
    price = FloatField('Kaina', validators=[DataRequired(), NumberRange(min=0.01)])
    stock = IntegerField('Kiekis sandėlyje', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Pridėti prekę')
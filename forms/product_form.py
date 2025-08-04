from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, FloatField, SelectField, FileField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.validators import  DataRequired, Length, NumberRange, Optional


class AddProductForm(FlaskForm):
    name = StringField('Prekės pavadinimas', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Aprašymas')
    price = FloatField('Kaina', validators=[DataRequired(), NumberRange(min=0.01)])
    stock = IntegerField('Kiekis sandėlyje', validators=[DataRequired(), NumberRange(min=0)])
    image = FileField('Nuotrauka', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Tik paveikslėliai'),FileRequired('Prašome įkelti nuotrauką.')])
    submit = SubmitField('Pridėti prekę')


class UpdateProductForm(FlaskForm):
    name = StringField('Prekės pavadinimas', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Aprašymas')
    price = FloatField('Kaina', validators=[DataRequired(), NumberRange(min=0.01)])
    stock = IntegerField('Kiekis sandėlyje', validators=[DataRequired(), NumberRange(min=0)])
    image = FileField('Nuotrauka', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Tik paveikslėliai')])
    is_active = SelectField('Būsena', choices=[('1', 'Pardavime'), ('0', 'Išimta')], validators=[DataRequired(),Optional()])
    submit = SubmitField('Atnaujinti prekę')
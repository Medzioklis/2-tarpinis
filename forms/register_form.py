from flask_wtf import FlaskForm           # reikialinga instalint pip install flask-wtf
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, Length

class RegisterForm(FlaskForm):
    name = StringField('Vardas', validators=[DataRequired()])
    lastname = StringField('Pavardė', validators=[DataRequired()])
    email = StringField('El. paštas', validators=[DataRequired(), Email()])
    password1 = PasswordField('Slaptažodis',validators=[DataRequired('Slaptažodis būtinas'), Length(min=8, message='Slaptažodis turi būti bent 8 simbolių ilgio')])
    password2 = PasswordField('Slaptažodis',validators=[DataRequired('Slaptažodis būtinas'), Length(min=8, message='Slaptažodis turi būti bent 8 simbolių ilgio')])
    submit = SubmitField('Priregistruoti')


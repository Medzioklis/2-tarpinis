from flask_wtf import FlaskForm           # reikialinga instalint pip install flask-wtf
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Email, DataRequired

class RegisterForm(FlaskForm):
    name = StringField('Vardas', validators=[DataRequired()])
    lastname = StringField('Pavardė', validators=[DataRequired()])
    email = StringField('El. paštas', validators=[DataRequired(), Email()])
    password = PasswordField('Slaptažodis',validators=[DataRequired('Slaptažodis būtinas')])
    submit = SubmitField('Registruotis')


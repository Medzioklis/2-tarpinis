from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email, DataRequired

class LoginForm(FlaskForm):
    email = StringField('El. paštas', validators=[DataRequired(), Email()])
    password = PasswordField('Slaptažodis',validators=[DataRequired()])
    remember_me = BooleanField('Prisiminti mane')
    submit = SubmitField('Prisijungti')
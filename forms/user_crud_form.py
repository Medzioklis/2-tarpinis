from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from models.user_class import User 
from sqlalchemy import select
from database import db 

class AddUserForm(FlaskForm):
    """Forma naujo vartotojo pridėjimui (Admin)."""
    user_name = StringField('Vardas', validators=[DataRequired()])
    user_lastname = StringField('Pavardė', validators=[DataRequired()])
    user_email = StringField('El. paštas', validators=[DataRequired(), Email()])
    user_role = SelectField('Rolė', choices=[('2', 'Vartotojas'), ('1', 'Administratorius')], validators=[DataRequired()])
    password = PasswordField('Slaptažodis', validators=[
        DataRequired(),
        Length(min=8, message='Slaptažodis turi būti bent 8 simbolių ilgio.')
    ])
    confirm_password = PasswordField('Pakartoti slaptažodį', validators=[
        DataRequired(),
        EqualTo('password', message='Slaptažodžiai turi sutapti.')
    ])
    submit = SubmitField('Pridėti vartotoją')


class UpdateUserForm(FlaskForm):
    """Forma esamo vartotojo redagavimui (Admin)."""
    user_name = StringField('Vardas', validators=[DataRequired()])
    user_lastname = StringField('Pavardė', validators=[DataRequired()])
    user_email = StringField('El. paštas', validators=[DataRequired(), Email()])
    user_role = SelectField('Rolė', choices=[('2', 'Vartotojas'), ('1', 'Administratorius')], validators=[DataRequired()])
    submit = SubmitField('Atnaujinti duomenis')

    def __init__(self, original_email, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_user_email(self, user_email):
        """Tikrina, ar naujas el. paštas unikalus (išskyrus paties vartotojo)."""
        if user_email.data != self.original_email:
            stmt = select(User).where(User.user_email == user_email.data)
            user = db.session.execute(stmt).scalar_one_or_none()
            if user:
                raise ValidationError('Šis el. pašto adresas jau naudojamas.')

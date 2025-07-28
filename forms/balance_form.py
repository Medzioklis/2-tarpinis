
from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class BalanceForm(FlaskForm):
    amount = DecimalField('Suma (€)', validators=[DataRequired(), NumberRange(min=0.01)], places=2)
    submit = SubmitField('Papildyti balansą')

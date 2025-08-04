from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length

class ReviewForm(FlaskForm):
    rating = IntegerField('Įvertinimas (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    text = TextAreaField('Atsiliepimas', validators=[Length(max=500)])
    submit = SubmitField('Pateikti atsiliepimą')
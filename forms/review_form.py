from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ReviewForm(FlaskForm):
    rating = IntegerField('Įvertinimas (1–5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Atsiliepimas', render_kw={"rows": 4})
    submit = SubmitField('Pateikti atsiliepimą')
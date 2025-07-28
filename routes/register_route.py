from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user
from sqlalchemy import select
from forms.register_form import RegisterForm
from models.user_class import User
from werkzeug.security import generate_password_hash
from database import db

register_bp = Blueprint('register', __name__, url_prefix='/register', template_folder='../templates')

@register_bp.route('/', methods=['GET', 'POST'])
def register():
    # Jei vartotojas jau prisijungęs, nukreipiame jį į pagrindinį puslapį
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        # tikrinam ar email nesidubliuoja
        user_email = select(User).where(User.user_email == form.email.data)
        existing_user_email = db.session.scalars(user_email).first()
        if existing_user_email:
            flash("Šis el. pašto adresas jau užimtas. Pasirinkite kitą.")
            return redirect(url_for('register.register'))
        # tikrinam ar sutampa slaptazodziu laukai
        if form.password1.data != form.password2.data:
            flash("Slaptažodžių laukai nesutampa.")
            return redirect(url_for('register.register'))   
        # Užkoduojame slaptažodį
        hashed_password = generate_password_hash(form.password1.data).encode('utf-8')
        # Sukuriame naują vartotoją
        new_user = User(user_name=form.name.data, user_lastname=form.lastname.data,  user_email=form.email.data, user_password=hashed_password)
        # Įrašome į duomenų bazę
        db.session.add(new_user)
        db.session.commit()
        flash(f'Paskyra sukurta sėkmingai! Dabar galite prisijungti.', 'success')
        return redirect(url_for('login.login'))
    return render_template('register.html', form=form)
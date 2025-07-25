from flask import render_template, flash
from werkzeug.security import generate_password_hash
from sqlalchemy import select
from database import db
from models.user_class import User
from forms.register_form import RegisterForm

def add_user():
    form = RegisterForm()
    if form.validate_on_submit():
        stmt = db.select(User).where(User.user_email == form.email.data)
        form_email = db.session.execute(stmt).scalar_one_or_none()
        if form_email is None:
            name = form.name.data
            lastname = form.lastname.data
            email = form.email.data
            password1 = form.password1.data
            password2 = form.password2.data
            if password1 == password2:
                password = generate_password_hash(password1, method='pbkdf2:sha256')
            else:
                flash("Slaptažodžiai nesutampa!", 'alert')
                return render_template('add_user.html', form=form)
            new_user = User(user_name=name, user_lastname=lastname, user_email=email, user_password=password)
            db.session.add(new_user)
            db.session.commit()
            return render_template('admin.html', user=new_user)
        else:
            flash("Vartotojas su tokiu el. paštu jau egzistuoja.", 'alert')
            return render_template('add_user.html', form=form)
    return render_template('add_user.html', form=form)

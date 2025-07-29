from werkzeug.security import generate_password_hash
from models.user_class import User, db
from sqlalchemy import select

def get_all_users():
    """Gražina visų vartotojų sąrašą."""
    return db.session.execute(select(User)).scalars().all()

def get_user_by_id(user_id):
    """Gražina vartotoją pagal ID."""
    return db.session.get(User, user_id)

def add_new_user(form):
    """Sukuriamas ir išsaugomas naujas vartotojas."""
    new_user = User(
        user_name=form.user_name.data,
        user_lastname=form.user_lastname.data,
        user_email=form.user_email.data,
        user_role=int(form.user_role.data),
        user_password=generate_password_hash(form.password.data)
    )
    db.session.add(new_user)
    db.session.commit()

def update_existing_user(user, form):
    """Atnaujinami esamo vartotojo duomenys."""
    user.user_name = form.user_name.data
    user.user_lastname = form.user_lastname.data
    user.user_email = form.user_email.data
    user.user_role = int(form.user_role.data)
    db.session.commit()

def delete_user_by_id(user_id):
    """Ištrinamas vartotojas pagal ID."""
    user = get_user_by_id(user_id)
    if user:
        if user.user_role == 1: # Apsauga, kad nebūtų galima ištrinti admino
            return False, "Negalima ištrinti administratoriaus."
        db.session.delete(user)
        db.session.commit()
        return True, f"Vartotojas '{user.user_name}' sėkmingai ištrintas."
    return False, "Vartotojas nerastas."

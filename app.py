from flask import render_template
# from sqlalchemy import and_, select
# from werkzeug.security import generate_password_hash, check_password_hash

from config import app, db
from models.user_class import User
from forms.register_form import RegisterForm

@app.route('/')
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        lastname = form.lastname.data
        email = form.email.data
        password = form.password.data

        new_user = User(user_name = name, user_lastname = lastname, user_email = email, user_password = password, createdBy = form.email.data)
        db.session.add(new_user)
        db.session.commit()
        message = 'Registracija sekminga !'
        return render_template('admin.html')
    else:
        return render_template('register.html', message=message, form=form)


# # run code in debug mode
# if __name__ == "__main__":
#     app.run(debug=True)

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import text

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mrka_esu:labas123@cloud.prisijungimas.lt:3306/mrka_eshop?ssl=True'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# def check_db_connection():
#     try:
#         # Bandymas prisijungti ir vykdyti paprastą užklausą
#         with app.app_context():
#             with db.engine.connect() as connection:
#                 result = connection.execute(text("SELECT VERSION()"))
#                 version = result.fetchone()[0]
#                 print(f"Prisijungimas sėkmingas! MariaDB versija: {version}")
#                 return True
#     except Exception as e:
#         print(f"Prisijungimo klaida: {e}")
#         return False

# if __name__ == '__main__':
#     # Patikriname prisijungimą paleidimo metu
#     check_db_connection()
#     app.run(debug=True)
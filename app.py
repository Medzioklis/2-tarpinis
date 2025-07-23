from database import app, db
from flask_login import LoginManager
from models.user import User
from models.admin import Admin

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id)) or db.session.get(Admin, int(user_id))

import services.login


if __name__ == '__main__':
    app.run(debug=True)
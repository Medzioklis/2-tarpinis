from database import app, db
from flask_login import LoginManager
from models.user import User
from flask_migrate import Migrate

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


import services.login

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)
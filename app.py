from database import app
from routes.home import home_bp
from routes.admin import admin_bp
from routes.user import user_bp
from routes.auth import auth_bp
from routes.product import product_bp
from routes.stats import stats_bp





app.register_blueprint(home_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(product_bp)
app.register_blueprint(stats_bp)


if __name__ == "__main__":
    app.run(debug=True)
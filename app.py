from flask import Flask
from routes.products import products_bp

app = Flask(__name__)
app.secret_key = 'slaptas_raktas'

app.register_blueprint(products_bp)

if __name__ == '__main__':
    app.run(debug=True)
    
from flask import render_template
from database import app
from services.user_functions import add_user

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['GET', 'POST'])
def register():
    return add_user()

if __name__ == "__main__":
    app.run(debug=True)
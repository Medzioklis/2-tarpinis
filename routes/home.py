from flask import Blueprint, redirect, url_for, render_template 

home_bp = Blueprint('home', __name__, url_prefix='/', template_folder='../templates')

@home_bp.route('/')
def index():
    return render_template('index.html')
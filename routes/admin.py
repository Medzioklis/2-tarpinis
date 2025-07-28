from flask import Blueprint, render_template, flash, redirect, url_for
from services.user_functions import admin_required
from models.user_class import User
from sqlalchemy import select, func
from database import db


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard')
def dashboard():
    admin_required()
    try:
        stats = {
            'user_count': db.session.scalar(select(func.count(User.id)))
            # 'product_count': product_service.Product.query.count(),
            # 'total_sales': db.session.query(db.func.sum(Order.total_price)).scalar() or 0
        }
        return render_template('admin/dashboard.html', title='Admin Panelė', stats=stats)
    except Exception as e:
        flash(f"Klaida gaunant statistiką: {e}", "danger")
        return render_template('admin/dashboard.html', title='Admin Panelė', stats={'user_count': 0, 'product_count': 0, 'total_sales': 0})
    
@admin_bp.route('/users')
def user_list():
    try:
        all_users = db.session.scalars(select(User)).all()
        return render_template('admin/users.html', title='Vartotojai', users=all_users)
    except Exception as e:
        flash(f"Klaida gaunant vartotojų sąrašą: {e}", "danger")
        return render_template('admin/users.html', title='Vartotojai', users=[])
    
@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    admin_required()
    try:
        user = db.session.get(User, user_id)
        if not user:
            flash("Vartotojas nerastas.", "danger")
            return redirect(url_for('admin.user_list'))
        # Patikriname, ar vartotojas yra administratorius
        if user.user_role == 1:
            flash("Negalima ištrinti administratoriaus.", "danger")
        else:
            db.session.delete(user)
            db.session.commit()
            flash(f"Vartotojas '{user.user_name} {user.user_lastname}' sėkmingai ištrintas.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Klaida trinant vartotoją: {e}", "danger")
    return redirect(url_for('admin.user_list'))
   
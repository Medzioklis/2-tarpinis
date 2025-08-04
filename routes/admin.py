from flask import Blueprint, render_template, redirect, url_for, flash, request
from forms.user_crud_form import AddUserForm, UpdateUserForm, db 
from services import admin_services 
from services.auth_functions import admin_required
from sqlalchemy import select, func
from models.user_class import User
from models.product_class import Product
from models.order_class import Order


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
def dashboard():
    admin_required()
    try:
        stats = {
            'user_count': db.session.scalar(select(func.count(User.id)).where(User.deleted == False)),
            'product_count': db.session.scalar(select(func.count(Product.id)).where(Product.deleted == False)),
            'total_sales': db.session.scalar(select(func.sum(Order.total_price)).where(Order.deleted == False)) or 0
            
        }
        return render_template('admin/dashboard.html', title='Admin Panelė', stats=stats)
    except Exception as e:
        flash(f"Klaida gaunant statistiką: {e}", "danger")
        return render_template('admin/dashboard.html', title='Admin Panelė', stats={'user_count': 0, 'product_count': 0, 'total_sales': 0})
    
# ========================================= USER CRUD ===========================================================================================

# USER READ Vartotojų sąrašo rodymas
@admin_bp.route('/users')
def user_list():
    admin_required()
    try:
        users = admin_services.get_all_users()
        return render_template('admin/users.html', users=users, title="Vartotojų valdymas")
    except Exception as e:
        flash(f"Klaida gaunant vartotojų sąrašą: {e}", "danger")
        return render_template('admin/users.html', users=[], title="Vartotojų valdymas")

# USER CREATE: Naujo vartotojo pridėjimas
@admin_bp.route('/user_add', methods=['GET', 'POST'])
def user_add():
    admin_required()
    form = AddUserForm()
    if form.validate_on_submit():
        try:
            admin_services.add_new_user(form)
            flash('Naujas vartotojas sėkmingai pridėtas!', 'success')
            return redirect(url_for('admin.user_list'))
        except Exception as e:
            flash(f"Klaida pridedant vartotoją: {e}", "danger")
    return render_template('admin/add_user.html', form=form, title="Pridėti vartotoją")

# USER UPDATE: Vartotojo redagavimas
@admin_bp.route('/users/update/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    admin_required()
    user = admin_services.get_user_by_id(user_id)
    if not user:
        flash('Vartotojas nerastas.', 'danger')
        return redirect(url_for('admin.user_list'))
    
    form = UpdateUserForm(original_email=user.user_email)
    if form.validate_on_submit():
        try:
            admin_services.update_existing_user(user, form)
            flash('Vartotojo duomenys sėkmingai atnaujinti!', 'success')
            return redirect(url_for('admin.user_list'))
        except Exception as e:
            flash(f"Klaida atnaujinant duomenis: {e}", "danger")

    elif request.method == 'GET':
        form.user_name.data = user.user_name
        form.user_lastname.data = user.user_lastname
        form.user_email.data = user.user_email
        form.user_role.data = str(user.user_role)
        
    return render_template('admin/update_user.html', form=form, user=user, title="Redaguoti vartotoją")

# USER DELETE: Vartotojo ištrynimas
@admin_bp.route('/users/delete/<user_id>', methods=['POST'])
def delete_user(user_id):
    admin_required()
    try:
        success, message = admin_services.delete_user_by_id(user_id)
        if success:
            flash(message, 'success')
        else:
            flash(message, 'danger')
    except Exception as e:
        flash(f"Klaida trinant vartotoją: {e}", "danger")
    return redirect(url_for('admin.user_list'))

# ========================================= END USER CRUD =================================================================================

# ========================================= ORDER =========================================================================================

@admin_bp.route('/orders_list')
def orders_list():
    admin_required()
    try:
        orders = admin_services.get_all_orders()
        return render_template('admin/orders_view.html', orders=orders, title="Užsakymų sąrašas")
    except Exception as e:
        flash(f"Klaida gaunant užsakymų sąrašą: {e}", "danger")
        return render_template('admin/dashboard.html')

@admin_bp.route('/orders/delete/<order_id>' , methods=['POST'])
def order_delete(order_id):
    admin_required()
    try:
        order = db.session.get(Order, order_id)
        if order:
            order.deleted = True
            db.session.commit()
            flash(f"Užsakymas {order_id} sėkmingai ištrintas.", 'success')
        else:
            flash(f"Užsakymas {order_id} nerastas.", 'danger')
    except Exception as e:
        flash(f"Klaida trinant užsakymą: {e}", "danger")
    return redirect(url_for('admin.orders_list'))
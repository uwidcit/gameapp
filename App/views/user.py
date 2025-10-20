from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import (
    create_user,
    get_all_users,
    get_all_users_json,
    jwt_required,
    login_required
)

from App.models import User, Staff, Customer

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    user = create_user(data['username'], data['password'])
    return jsonify({'message': f"user {user.username} created with id {user.id}"})

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')

@user_views.route('/api/admin/users', methods=['GET'])
@login_required(User)
def get_users_admin_only():
    """
    Example route that requires the current user to be an instance of User class.
    This demonstrates the login_required decorator usage.
    """
    users = get_all_users_json()
    return jsonify({
        'message': 'Admin access granted', 
        'current_user': jwt_current_user.username,
        'users': users
    })

@user_views.route('/api/staff/manage', methods=['GET'])
@login_required(Staff)
def staff_only_route():
    """
    Example route that only staff members can access.
    Demonstrates polymorphic identity with login_required decorator.
    """
    from App.controllers import get_staff_json, get_customers_json
    
    return jsonify({
        'message': 'Staff access granted',
        'current_staff': jwt_current_user.username,
        'staff_members': get_staff_json(),
        'customers': get_customers_json(),
        'privileges': {
            'can_manage_listings': jwt_current_user.can_manage_listings(),
            'can_view_admin_panel': jwt_current_user.can_view_admin_panel()
        }
    })
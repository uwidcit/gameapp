from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from.index import index_views

from App.controllers import (
    jwt_required,
    login_required,
    create_customer,
    create_staff
)

from App.models import User, Staff, Customer

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    # create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')

@user_views.route('/api/customers', methods=['POST'])
def create_customer_api():
    data = request.json
    customer = create_customer(data['username'], data['password'])
    if customer:
        return jsonify({'message': f'Customer created successfully with ID: {customer.id}'}), 201
    return jsonify({'message': 'Error creating customer user'}), 400

@user_views.route('/api/staff', methods=['POST'])
def create_staff_api():
    data = request.json
    staff = create_staff(data['username'], data['password'], data['staff_id'])
    if staff:
        return jsonify({'message': f'Staff created successfully with ID: {staff.id}'}), 201
    return jsonify({'message': 'Error creating staff user'}), 400
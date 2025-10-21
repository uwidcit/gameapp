from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user
from App.models import Staff, Customer
from App.controllers import (login_required, staff_confirm_rental, staff_return_rental)

rental_views = Blueprint('rental_views', __name__, template_folder='../templates')


@rental_views.route('/api/rentals', methods=['POST'])
@login_required(Staff)
def create_rental_api():
    data = request.json
    rental  = staff_confirm_rental(staffId=current_user.id,
                                   customer_id=data['customer_id'],
                                   listing_id=data['listing_id'])
    if not rental:
        return jsonify({'message': f'Error creating rental'}), 400
    return jsonify({'message': f'Rental created successfully with ID: {rental.rental_id}'}), 201


@rental_views.route('/api/rentals/<int:rental_id>', methods=['PUT'])
@login_required(Staff)
def return_rental_api(rental_id):
    data = request.json
    rental = staff_return_rental(staffId=current_user.id, rental_id=rental_id)
    if not rental:
        return jsonify({'message': f'Error returning rental'}), 400
    return jsonify({'message': f'Rental returned successfully with ID: {rental.rental_id}'}), 200
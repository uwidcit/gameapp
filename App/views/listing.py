from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user
from App.models import Staff, Customer
from App.controllers import (login_required, staff_create_listing, get_available_listings, customer_change_listing_availability)

listing_views = Blueprint('listing_views', __name__, template_folder='../templates')    

@listing_views.route('/api/listings', methods=['POST'])
@login_required(Staff)
def create_listing_api():
    data = request.json
    listing = staff_create_listing(
        staff_id=current_user.id,
        game_id=data['game_id'],
        owner_id=data['owner_id'],
        price=data['price'],
        condition=data['condition']
    )
    if not listing:
        return jsonify({'message': f'Error creating listing'}), 400
    return jsonify({'message': f'Listing created successfully with ID: {listing.listing_id}'}), 201

@listing_views.route('/api/listings', methods=['GET'])
def get_listings_api():
    listings = get_available_listings()
    listings_data = [ listing.get_json() for listing in listings]
    return jsonify(listings_data), 200

@listing_views.route('/api/listings/<int:listing_id>/availability', methods=['PUT'])
@login_required(Customer)
def change_listing_availability_api(listing_id):
    data = request.json
    new_availability = data.get('availability')
    if new_availability is None:
        return jsonify({'message': 'Availability status is required'}), 400
    listing = customer_change_listing_availability(customer_id=current_user.id, listing_id=listing_id, available=new_availability)
    if not listing:
        return jsonify({'message': f'Error changing availability for listing {listing_id}'}), 400
    return jsonify({'message': f'Listing {listing_id} availability updated successfully'}), 200
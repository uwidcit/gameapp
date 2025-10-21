from App.models import Rental, Staff, Customer, Listing
from App.database import db


def staff_confirm_rental(staffId, customer_id, listing_id):
    staff = Staff.query.get(staffId)
    customer = Customer.query.get(customer_id)
    listing = Listing.query.get(listing_id)

    if not staff or not customer or not listing:
        return None # Invalid IDs provided

    new_rental = staff.create_rental(customer, listing)
    return new_rental

def staff_return_rental(staffId, rental_id):
    staff = Staff.query.get(staffId)
    rental = Rental.query.get(rental_id)
    if not staff or not rental:
        return None # Invalid IDs provided

    staff.return_rental(rental)
    return rental
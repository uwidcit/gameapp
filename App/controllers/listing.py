from App.models import Listing
from App.database import db
from App.models import Staff, Game, Listing, Customer


def get_all_listings():
    """Retrieve all listings"""
    return Listing.query.all()

def get_available_listings():
    """Retrieve all available listings"""
    return Listing.query.filter_by(available=True).all()

def staff_create_listing(staff_id, game_id, owner_id, price, condition):
    staff = db.session.get(Staff, staff_id)
    game = db.session.get(Game, game_id)
    owner = db.session.get(Customer, owner_id)

    if not staff or not game or not owner:
        print(f"Invalid staff, game, or owner ID staff: {staff_id}, game: {game_id}, owner: {owner_id}")
        return None

    listing = staff.create_listing(owner, game, price, condition)
    return listing

def customer_change_listing_availability(customer_id, listing_id, available):
    # Retrieve the listing filtering by listing_id and owner_id
    listing = Listing.query.filter_by(listing_id=listing_id, owner_id=customer_id).first()
    if listing:
        listing.set_availability(available)
        db.session.commit()
        return listing
    return None
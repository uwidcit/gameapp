from App.database import db

class Rental(db.Model):
    rental_id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.listing_id'), nullable=False)
    renter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rental_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    return_date = db.Column(db.DateTime, nullable=True)

    listing = db.relationship('Listing', backref=db.backref('rentals', lazy=True))
    renter = db.relationship('User', backref=db.backref('rentals', lazy=True))

    def __init__(self, listing_id, renter_id):
        self.listing_id = listing_id
        self.renter_id = renter_id
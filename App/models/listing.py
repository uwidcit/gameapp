from App.database import db

class Listing(db.Model):
    listing_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(50), nullable=True)
    available = db.Column(db.Boolean, default=True)

    game = db.relationship('Game', backref=db.backref('listings', lazy=True))
    user = db.relationship('User', backref=db.backref('listings', lazy=True))

    def __init__(self, game_id, owner_id, price, condition):
        self.game_id = game_id
        self.owner_id = owner_id
        self.price = price
        self.condition = condition

    def set_availability(self, available):
        self.available = available
    
    def get_json(self):
        return {
            'listing_id': self.listing_id,
            'game title': self.game.title,
            'owner_id': self.owner_id,
            'owner_username': self.user.username,
            'price': self.price,
            'condition': self.condition,
            'available': self.available
        }
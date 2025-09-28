from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from .listing import Listing


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def list_game(self, game, price, condition):
        new_listing = Listing(game_id=game.id, owner_id=self.id, price=price, condition=condition)
        self.listings.append(new_listing)
        db.session.add(new_listing)
        db.session.commit()
        return new_listing

    def __repr__(self):
        return f'<User {self.id} - {self.username}>'

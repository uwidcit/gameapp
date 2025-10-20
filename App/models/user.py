from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from .listing import Listing


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': user_type,
        'with_polymorphic': '*'
    }

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


class Staff(User):
    """Staff user with administrative privileges"""
    
    __mapper_args__ = {
        'polymorphic_identity': 'staff'
    }
    
    def __init__(self, username, password):
        super().__init__(username, password)
    
    def get_json(self):
        json_data = super().get_json()
        json_data['user_type'] = 'staff'
        return json_data
    
    def can_manage_listings(self):
        """Staff can manage all listings"""
        return True
    
    def can_view_admin_panel(self):
        """Staff can view admin panel"""
        return True
    
    def __repr__(self):
        return f'<Staff {self.id} - {self.username}>'


class Customer(User):
    """Customer user with standard privileges"""
    
    __mapper_args__ = {
        'polymorphic_identity': 'customer'
    }
    
    def __init__(self, username, password):
        super().__init__(username, password)
    
    def get_json(self):
        json_data = super().get_json()
        json_data['user_type'] = 'customer'
        return json_data
    
    def can_manage_listings(self):
        """Customers can only manage their own listings"""
        return False
    
    def can_view_admin_panel(self):
        """Customers cannot view admin panel"""
        return False
    
    def __repr__(self):
        return f'<Customer {self.id} - {self.username}>'

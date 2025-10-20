from App.models import User, Staff, Customer
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def create_staff(username, password):
    """Create a new staff user"""
    newstaff = Staff(username=username, password=password)
    db.session.add(newstaff)
    db.session.commit()
    return newstaff

def create_customer(username, password):
    """Create a new customer user"""
    newcustomer = Customer(username=username, password=password)
    db.session.add(newcustomer)
    db.session.commit()
    return newcustomer

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def get_all_staff():
    """Get all staff users"""
    return db.session.scalars(db.select(Staff)).all()

def get_all_customers():
    """Get all customer users"""
    return db.session.scalars(db.select(Customer)).all()

def get_staff_json():
    """Get all staff users as JSON"""
    staff = get_all_staff()
    if not staff:
        return []
    return [user.get_json() for user in staff]

def get_customers_json():
    """Get all customer users as JSON"""
    customers = get_all_customers()
    if not customers:
        return []
    return [user.get_json() for user in customers]

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None

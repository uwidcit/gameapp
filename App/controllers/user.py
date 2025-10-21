from App.models import User, Staff, Customer
from App.database import db


def create_staff(username, password, staff_id):
    """Create a new staff user"""
    newstaff = Staff(username=username, password=password, staff_id=staff_id)
    try:
        db.session.add(newstaff)
        db.session.commit()
        return newstaff
    except Exception as e:
        db.session.rollback()
        print(f"Error creating staff user: {e}")
        return None

def create_customer(username, password):
    """Create a new customer user"""
    newcustomer = Customer(username=username, password=password)
    try:
        db.session.add(newcustomer)
        db.session.commit()
        return newcustomer
    except Exception as e:
        db.session.rollback()
        print(f"Error creating customer user: {e}")
        return None

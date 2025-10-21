import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Staff, Customer
from App.controllers import (
 
    create_staff,
    create_customer,

    login,
    get_user,
    get_user_by_username,
    update_user
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        user = User("bob", password)
        # Simply verify that the password is hashed (not stored as plaintext)
        assert user.password != password
        # Verify that the password is properly hashed using scrypt (Werkzeug's default)
        assert user.password.startswith('scrypt:')

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()



class UsersIntegrationTests(unittest.TestCase):


    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

    def test_login_required_decorator(self):
        from App.controllers.auth import login_required
        from App.models import User
        from flask import Flask, jsonify
        from flask_jwt_extended import create_access_token, JWTManager
        
        # Create a test app for this specific test
        test_app = Flask(__name__)
        test_app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        jwt = JWTManager(test_app)
        
        # Create a mock class for testing
        class AdminUser:
            pass
        
        # Create test route with login_required decorator
        @test_app.route('/test-admin')
        @login_required(AdminUser)
        def test_admin_route():
            return jsonify({'message': 'Admin access granted'})
        
        with test_app.test_client() as client:
            # Test without authentication should fail
            response = client.get('/test-admin')
            assert response.status_code == 401

    def test_identify_route_shows_user_type(self):
        """Test that the identify route returns user type information"""
        from App.main import create_app
        from App.controllers import login
        
        app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
        
        # Create a staff user for testing
        staff_user = create_staff('teststaff2', 'staffpass')
        
        with app.test_client() as client:
            # Login as staff user
            login_response = client.post('/api/login', 
                json={'username': 'teststaff2', 'password': 'staffpass'})
            assert login_response.status_code == 200
            
            # Test identify endpoint
            identify_response = client.get('/api/identify')
            assert identify_response.status_code == 200
            
            data = identify_response.get_json()
            assert 'user' in data
            assert data['user']['username'] == 'teststaff2'
            assert data['user']['user_type'] == 'staff'

    def test_polymorphic_staff_creation(self):
        staff = create_staff("teststaff1", "staffpass")
        assert staff.username == "teststaff1"
        assert isinstance(staff, Staff)
        assert staff.user_type == "staff"
        assert staff.can_manage_listings() == True
        assert staff.can_view_admin_panel() == True

    def test_polymorphic_customer_creation(self):
        customer = create_customer("testcustomer1", "customerpass")
        assert customer.username == "testcustomer1"
        assert isinstance(customer, Customer)
        assert customer.user_type == "customer"
        assert customer.can_manage_listings() == False
        assert customer.can_view_admin_panel() == False

    def test_polymorphic_json_serialization(self):
        staff = create_staff("jsonstaff1", "pass123")
        customer = create_customer("jsoncustomer1", "pass456")
        
        staff_json = staff.get_json()
        customer_json = customer.get_json()
        
        assert staff_json['user_type'] == 'staff'
        assert customer_json['user_type'] == 'customer'
        assert 'username' in staff_json
        assert 'username' in customer_json
        


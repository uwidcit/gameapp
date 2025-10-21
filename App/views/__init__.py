# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .listing import listing_views
from .rental import rental_views

views = [user_views, index_views, auth_views, listing_views, rental_views]
# blueprints must be added to this list
# blue prints are imported
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .student import student_views
from .review import review_views
from .karma import karma_views

views = [user_views, index_views, auth_views, student_views, review_views, karma_views]
# blueprints must be added to this list

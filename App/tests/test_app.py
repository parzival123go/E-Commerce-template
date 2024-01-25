import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from App.main import create_app
from App.database import db, create_db
from App.models import *
from App.controllers import *

LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob123", "bob", "bobpass")
        assert user.staff_id == "bob123"
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob123", "bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id": None, "staff_id": "bob123", "username": "bob"})

    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob123", "bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob123", "bob", password)
        assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and reused for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

def test_authenticate():
    user = create_user("bob123", "bob", "bobpass")
    assert login("bob", "bobpass") is not None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick123", "rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id": 1, "staff_id": "bob123", "username": "bob"}, {"id": 2, "staff_id": "rick123", "username": "rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"


class StudentsIntegrationTests(unittest.TestCase):
    def test_create_student(self):
        student_controller = StudentController()
        result = student_controller.create_student("John", "Doe", "john@example.com", "123-456-7890")
        assert result is True  # Check that student creation was successful

    def test_update_student(self):
        # Create a student first
        student_controller = StudentController()
        student_controller.create_student("John", "Doe", "john@example.com", "123-456-7890")

        # Get the student ID (assuming it's the first student created)
        student = db.session.query(Student).first()
        student_id = student.id

        # Update the student's first name
        updated_name = "Jane"
        student_controller = StudentController()
        result = student_controller.update_student(student_id, {"first_name": updated_name})
        assert result is True  # Check that student update was successful

        # Retrieve the updated student and verify the first name
        updated_student = db.session.query(Student).get(student_id)
        assert updated_student.first_name == updated_name


class ReviewsIntegrationTests(unittest.TestCase):
    def test_create_review(self):
        student_controller = StudentController()
        review_controller = ReviewController()

        # Create a student first
        student_controller.create_student("John", "Doe", "john@example.com", "123-456-7890")

        # Get the student ID (assuming it's the first student created)
        student = db.session.query(Student).first()
        student_id = student.id

        # Create a review
        message = "A great student"
        staff_id = 1  # Replace with a valid staff ID
        result = review_controller.create_log_review(student_id, message, staff_id)

        assert result is not None  # Check that the review creation was successful

    def test_search_reviews_by_student(self):
        student_controller = StudentController()
        review_controller = ReviewController()

        # Create a student first
        student_controller.create_student("John", "Doe", "john@example.com", "123-456-7890")

        # Get the student ID (assuming it's the first student created)
        student = db.session.query(Student).first()
        student_id = student.id

        # Create a review
        message = "A great student"
        staff_id = 1  # Replace with a valid staff ID
        review_controller.create_log_review(student_id, message, staff_id)

        # Search for reviews by student ID
        result = review_controller.search_reviews_by_student(student_id)

        assert result is not None  # Check that reviews were found

        # Verify that the retrieved review contains the correct message
        review = result[0]  # Assuming only one review was created
        assert review["message"] == message

@pytest.fixture(scope="module")
def app():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    app.app_context().push()
    db.create_all()

    yield app

    db.drop_all()
    app.app_context().pop()

def test_create_karma_vote(app):
    # Create a test review
    review = Reviews(student_id=1, message="A review for testing", staff_id=1)
    db.session.add(review)
    db.session.commit()

    # Test creating a karma vote for the review
    staff_id = 2
    review_id = review.id
    value = 1
    karma_vote = create_karma_vote(staff_id, review_id, value)

    assert karma_vote is not None

def test_calculate_karma_from_review(app):
    # Create a test review
    review = Reviews(student_id=1, message="Another review for testing", staff_id=1)
    db.session.add(review)
    db.session.commit()

    # Create karma votes for the review
    staff_id_1 = 2
    staff_id_2 = 3
    review_id = review.id

    # Staff member 1 gives +1 karma
    create_karma_vote(staff_id_1, review_id, 1)
    # Staff member 2 gives -1 karma
    create_karma_vote(staff_id_2, review_id, -1)

    # Test calculating karma for the review
    karma = calculate_karma_from_review(review_id)

    assert karma == 0  # Total karma should be 0
@pytest.mark.usefixtures('app')
def test_calculate_student_karma():
    # Create a test student
    student_id = 1
    student_karma = 5
    student = create_student(student_id, "John", "Doe", "john@example.com", "123-456-7890", student_karma)

    # Create test reviews
    review_1 = Reviews(student_id=student_id, message="Review 1", staff_id=2)
    review_2 = Reviews(student_id=student_id, message="Review 2", staff_id=3)
    db.session.add(review_1)
    db.session.add(review_2)
    db.session.commit()

    # Create karma votes for reviews
    review_id_1 = review_1.id
    review_id_2 = review_2.id

    create_karma_vote(2, review_id_1, 1)  # +1 karma for review 1
    create_karma_vote(3, review_id_2, -1)  # -1 karma for review 2

    # Test calculating karma for the student
    total_karma = calculate_student_karma(student_id)

    assert total_karma == 0  # Total karma for the student should be 0




# Helper function to create a student with a predefined karma score
def create_student(first_name, last_name, email, phone_number, karma_score):
    student = Student(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, karma_score=karma_score)
    db.session.add(student)
    db.session.commit()
    return student


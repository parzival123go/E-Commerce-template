from App.database import db
from App.models.review import Reviews


class ReviewController:
    def create_log_review(self, student_id, message, staff_id):
        try:
            # Create a new review instance
            new_review = Reviews(
                student_id=student_id,
                message=message,
                staff_id=staff_id
            )

            # Add the new review to the database
            db.session.add(new_review)
            db.session.commit()

            return new_review  # Return the created review object
        except Exception as e:
            # Handle any exceptions (e.g., database errors) here
            print(str(e))
            db.session.rollback()  # Rollback changes in case of an error
            return None  # Review creation failed

    def search_reviews_by_student(self, student_id):
        try:
            # Query for reviews with the specified student_id
            reviews = Reviews.query.filter_by(student_id=student_id).all()

            if reviews:
                # Return a list of review information as dictionaries
                review_info_list = []
                for review in reviews:
                    review_info = {
                        'id': review.id,
                        'student_id': review.student_id,
                        'message': review.message,
                        'staff_id': review.staff_id
                    }
                    review_info_list.append(review_info)
                return review_info_list
            else:
                return None  # No reviews found for the student
        except Exception as e:
            # Handle any exceptions (e.g., database errors) here
            print(str(e))
            return None  # Search operation failed

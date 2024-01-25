from App.database import db
from App.models.review import Reviews
from App.models.user import User
from App.models.student import Student
from App.models.karmaranking import KarmaVote


def create_karma_vote(staff_id, review_id, value):
  try:
    # Check if the staff member has already voted on the review
    existing_vote = KarmaVote.query.filter_by(staff_id=staff_id,
                                              review_id=review_id).first()
    new_vote = None  # Initialize new_vote as None

    if existing_vote:
      # Update the vote if it's different from the previous vote
      if existing_vote.value != value:
        existing_vote.value = value
        db.session.add(existing_vote)
        db.session.commit()
    else:
      # Create a new vote
      new_vote = KarmaVote(staff_id=staff_id, review_id=review_id, value=value)
      db.session.add(new_vote)
      db.session.commit()

    # Calculate karma for the student who received the review
    student_id = get_student_id_from_review(review_id)
    calculate_student_karma(student_id)

    return new_vote
  except Exception as e:
    print(str(e))
    db.session.rollback()
    return None


def get_student_id_from_review(review_id):
  review = Reviews.query.get(review_id)
  if review:
    return review.student_id
  return None


def calculate_student_karma(student_id):
  try:
    # Retrieve all reviews authored by the student
    reviews = Reviews.query.filter_by(student_id=student_id).all()

    if reviews:
      total_karma = 0

      # Calculate karma for each review based on karma votes
      for review in reviews:
        review_id = review.id
        karma = calculate_karma_from_review(review_id)
        total_karma += karma

      # Update the student's karma attribute with the total karma
      student = Student.query.get(student_id)
      student.karma_score = total_karma
      db.session.add(student)
      db.session.commit()

      return total_karma
    else:
      # No reviews found for the student
      return 0
  except Exception as e:
    print(str(e))
    db.session.rollback()
    return None


def calculate_karma_from_review(review_id):
  try:
    # Retrieve all karma votes associated with the review
    karma_votes = KarmaVote.query.filter_by(review_id=review_id).all()

    total_karma = 0

    # Calculate karma for the review based on karma votes
    for vote in karma_votes:
      total_karma += vote.value

    return total_karma
  except Exception as e:
    print(str(e))
    return 0  # Return 0 karma in case of an error

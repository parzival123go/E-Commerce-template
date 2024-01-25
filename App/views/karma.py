from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from .index import index_views

from App.controllers import (create_user, jwt_authenticate, get_all_users,
                             get_user_by_username, get_all_users_json,
                             jwt_required)

karma_views = Blueprint('karma_views', __name__, template_folder='../templates')


from App.controllers import ReviewController
from App.controllers import StudentController

student_controller = StudentController()
review_controller = ReviewController()

#karma
from App.models.review import Reviews
from App.controllers import create_karma_vote


@karma_views.route('/api/reviews/<int:review_id>/karma', methods=['POST'])
@jwt_required()
def karma_ranking(review_id):
  try:
    # Get the logged-in staff member's ID from the JWT token
    staff_id = jwt_current_user.id
    #staff_id = 2  #todo change this to jwt identify

    # Get the JSON data from the request
    data = request.get_json()

    # Check if the required field 'value' is present in the request JSON
    if 'value' not in data:
      return jsonify({"error": "Invalid request payload"}), 400

    # Extract the 'value' field from the request JSON
    value = data['value']

    # Ensure 'value' is either 1 (upvote) or -1 (downvote)
    if value not in [1, -1]:
      return jsonify({"error": "Invalid 'value' field"}), 400

    # Call the create_karma_vote function to create or update a karma vote
    new_vote = create_karma_vote(staff_id, review_id, value)

    if new_vote:
      return jsonify({"message": "Karma vote recorded successfully"}), 201
    else:
      return jsonify({"error": "Failed to record karma vote, staff already voted"
                      }), 500
  except Exception as e:
    # Handle any exceptions (e.g., database errors) here
    print(str(e))
    return jsonify({"error": "Internal Server Error"}), 500

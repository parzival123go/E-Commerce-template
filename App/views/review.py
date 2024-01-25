from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from .index import index_views

from App.controllers import (create_user, jwt_authenticate, get_all_users,
                             get_user_by_username, get_all_users_json,
                             jwt_required)

review_views = Blueprint('review_views', __name__, template_folder='../templates')

from App.controllers import ReviewController

review_controller = ReviewController()


@review_views.route("/api/reviews/<int:student_id>", methods=["POST"])
@jwt_required()
def log_review(student_id):
  try:

    # Get the JSON data from the request
    data = request.get_json()

    # Check if the required fields are present in the request
    if "message" not in data:
      return jsonify({"error": "Invalid request payload"}), 400

    # Extract review data from the request
    message = data["message"]

    staff_id = jwt_current_user.id
    # Call the create_log_review method from the ReviewController
    new_review = review_controller.create_log_review(student_id, message,
                                                     staff_id)

    if new_review:
      # If the review is created successfully, return a success response
      return jsonify({
          "message": "Review logged successfully",
          "review_id": new_review.id
      }), 201
    else:
      # If the review creation fails
      return jsonify({"error": "Review creation failed"
                      }), 500 

  except Exception as e:
    # Handle any exceptions (e.g., database errors) here
    print(str(e))
    return jsonify({"error": "Internal Server Error"}), 500


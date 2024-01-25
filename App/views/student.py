from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from .index import index_views

from App.controllers import (create_user, jwt_authenticate, get_all_users,
                             get_user_by_username, get_all_users_json,
                             jwt_required)

student_views = Blueprint('student_views', __name__, template_folder='../templates')


from App.controllers import StudentController

student_controller = StudentController()

@student_views.route('/api/search', methods=['GET'])
@jwt_required()
#@login_required
def search_student():
  try:
    # Get the student ID from the request JSON data
    data = request.get_json()
    student_id = data.get("studentID")

    if student_id is None:
      return jsonify({"error": "Invalid request payload"}), 400

    # Call the search_student method from the StudentController
    student_info = student_controller.search_student(student_id)

    if student_info:
      # If the student is found, return the student information
      return jsonify([{
          "studentID": student_info["student_id"],
          "firstName": student_info["first_name"],
          "lastName": student_info["last_name"],
          "email": student_info["email"],
          "phoneNumber": student_info["phone_number"]
      }]), 200
    else:
      # If the student is not found, return a 404 error
      return jsonify({"error": "Student not found"}), 404

  except Exception as e:
    # Handle any exceptions (e.g., database errors) here
    print(str(e))
    return jsonify({"error": "Internal Server Error"}), 500


@student_views.route("/api/students", methods=["POST"])
@jwt_required()  # You can apply authentication as needed
def add_student():
  try:
    # Parse the JSON request data
    data = request.get_json()

    # Check if the required fields are present in the request
    if "firstName" not in data or "lastName" not in data or "email" not in data or "phoneNumber" not in data:
      return jsonify({"error": "Invalid request payload"}), 400

    # Extract student data from the request
    first_name = data["firstName"]
    last_name = data["lastName"]
    email = data["email"]
    phone_number = data["phoneNumber"]

    # Call the create_student method from the StudentController
    result = student_controller.create_student(first_name, last_name, email,
                                               phone_number)
    
    student_id = student_controller.get_student_by_email(email)
    
    if result:
      return jsonify({
          "message": "Student added successfully",
          "studentID": str(student_id)
      }), 201
    else:
      return jsonify({"error": "Student creation failed"
                      }), 500 

  except Exception as e:
    # Handle any exceptions (e.g., database errors) here
    print(str(e))
    return jsonify({"error": "Internal Server Error"}), 500


@student_views.route("/api/update/<int:student_id>", methods=["POST"])
@jwt_required()
def update_student(student_id):
  try:
    # Get the JSON data from the request
    data = request.get_json()

    # Call the update_student method from the StudentController
    result = student_controller.update_student(student_id, data)

    if result:
      # If the student is updated successfully, return a success response
      return jsonify({"message": "Student updated successfully"}), 200
    else:
      # If the student is not found or update fails
      return jsonify({"error": "Student not found or update failed"
                      }), 400 

  except Exception as e:
    # Handle any exceptions (e.g., database errors) here
    print(str(e))
    return jsonify({"error": "Internal Server Error"}), 500


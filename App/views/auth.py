from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user

from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate,
    login 
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

'''
Page/Action Routes
'''

@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)


@auth_views.route('/identify', methods=['GET'])
@login_required
def identify_page():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})


@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    user = login(data['username'], data['password'])
    if user:
        login_user(user)
        return 'user logged in!'
    return 'bad username or password given', 401

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    data = request.form
    user = login(data['username'], data['password'])
    return 'logged out!'

'''
API Routes
'''

@auth_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)
#signup using default jwt
@auth_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    create_user(data['id'], data['username'], data['password'])
    return jsonify({'message': f"user {data['username']} created"})
#login using default jwt
@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = jwt_authenticate(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  return jsonify(access_token=token)

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
    return jsonify({'message': f"username: {jwt_current_user.username}, id : {jwt_current_user.id}"})






#trying with flask login

# from App.models.user import User
# from App.database import db

# @auth_views.route('/api/signup', methods=['POST'])
# def signup_action():
#     data = request.form  # Get data from form submission
#     staff_id = data['id']
#     username = data['username']
#     password = data['password']

#     # Check if a user with the same username already exists
#     existing_user = User.query.filter_by(username=username).first()

#     if existing_user:
#         flash("Username already exists. Please choose another username.")
#         return redirect(url_for('your_signup_route'))  # Redirect to your signup page

#     # Create a new user instance
#     new_user = User(staff_id=staff_id, username=username, password=password)

#     try:
#         # Add the new user to the database
#         db.session.add(new_user)
#         db.session.commit()  # Save the user
#         login_user(new_user)  # Log in the user
#         flash('Account Created!')  # Send a success message
#         return redirect(url_for('your_redirect_route'))  # Redirect to your homepage
#     except Exception as e:
#         # Handle any exceptions (e.g., database errors) here
#         print(str(e))
#         db.session.rollback()
#         flash("An error occurred while creating the account.")  # Error message
#     return redirect(url_for('your_signup_route'))  # Redirect to your signup page

# @auth_views.route('/login', methods=['POST'])
# def login_action2():
#     data = request.form
#     username = data['username']
#     password = data['password']

#     # Find the user by username
#     user = User.query.filter_by(username=username).first()

#     if user and user.check_password(password):  # Check credentials
#         login_user(user)  # Log in the user
#         flash('Logged in successfully.')  # Send a success message
#         return redirect(url_for('your_redirect_route'))  # Redirect to your main page after successful login
#     else:
#         flash('Invalid username or password')  # Send an error message
#     return redirect('/')  # Redirect to the login page
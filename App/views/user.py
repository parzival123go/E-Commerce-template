from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from .index import index_views

from App.controllers import (create_user, jwt_authenticate, get_all_users,
                             get_user_by_username, get_all_users_json,
                             jwt_required)

user_views = Blueprint('user_views', __name__, template_folder='../templates')


@user_views.route('/users', methods=['GET'])
def get_user_page():
  users = get_all_users()
  return render_template('users.html', users=users)


@user_views.route('/api/users', methods=['GET'])
def get_users_action():
  users = get_all_users_json()
  return jsonify(users)


@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
  data = request.json
  username = data.get('username')

  # Check if a user with the same username already exists
  existing_user = get_user_by_username(username)
  if existing_user:
    return jsonify(
        {'message': f"User with username {username} already exists"}), 400

  create_user(data['id'], data['username'], data['password'])
  return jsonify({'message': f"User {data['username']} created"}), 201

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')

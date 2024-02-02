import os
from datetime import timedelta
from flask import Flask, jsonify, request, render_template,flash,redirect
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from .models import db, User
from flask_login import LoginManager, current_user, login_user, login_required, logout_user


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    flash('Unauthorized!')
    return redirect(url_for('login'))

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'MySecretKey'
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
    CORS(app)
    db.init_app(app)
    login_manager.init_app(app) 
    app.app_context().push()
    return app

app = create_app()
jwt = JWTManager(app)  #setup flask jwt-e to work with app


#routes 
#To update
@app.route("/", methods=['GET'])   #gets the login page for either route hit
@app.route("/login", methods=['GET'])
def login():
   #return redirect(url_for('home_page'))
  return render_template("login.html")


@app.route('/home')
def index():
   return render_template("home.html")


@app.route('/signup')
def signup():
  return render_template("signup.html")


@app.route('/dashboard')
def dashboard():
  return render_template("dashboard.html")

@app.route("/login", methods=['POST'])
def login_func():
    data = request.form      #gets data entered by user (username, pw)
    user = User.query.filter_by(username = data['username']).first()    #finds matching entry
    if user and user.check_password(data['password']):
      login_user(user)    #if match found, log user in and redirect to their home page
      return redirect('/home')    
    else:
      flash('something wrong')    #else display error and redirect to login page again
      return redirect('/') 

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)

import os
from datetime import timedelta
from flask import Flask, jsonify, request, render_template,flash,redirect, url_for
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from .models import db, User, Product
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from werkzeug.utils import secure_filename
from flask import render_template



UPLOAD_FOLDER = '/uploads'

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
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
  return render_template("home.html")


@app.route('/home')
def home():
   return render_template("home.html")


@app.route("/signup", methods=['POST'])
def signup_user():
    data = request.form
    user = User.query.filter_by(email=data['email']).first()
    if user:
        flash("Email taken, please try again !!!")       
        return redirect(url_for('login') + '#getStarted')
    user = User(name=data['name'], email=data['email'], password=data['password'])
    flash("Account created for " + user.email)
    db.session.add(user)
    db.session.commit()
    return redirect('/dashboard')

@app.route("/logout", methods=['GET'])
@login_required
def logout_action():
  logout_user()      #logs out user and redirects to the main page (login page)
  #flash('Logging Out')
  return redirect('/')

@app.route('/dashboard', methods=['GET'])
def dashboard():
  return render_template("/product-admin/index.html")

@app.route('/orders')
def orders():
  return render_template("/dashboard/orders.html")

@app.route('/edit-product', methods=['GET']) 
def edit_product():
  return render_template("/product-admin/products.html")

@app.route('/products', methods=['GET']) 
def products():

  return render_template("/product-admin/products.html")

@app.route('/accounts', methods=['GET']) 
def accounts():
  return render_template("/product-admin/accounts.html")

@app.route('/add-product', methods=['GET','POST'])
def add_product():
    if request.method == 'POST':
      product_name = request.form['product_name']
      description = request.form['description']
      category = request.form['category']
      expire_date = request.form['expire_date']
      units_in_stock = request.form['units_in_stock']
      product = Product(product_name,description,category,expire_date, units_in_stock)
      db.session.add(product)
      db.session.commit()
      return "Successfuly added to database"
    else:
      return render_template("/product-admin/add-product.html")
 



@app.route("/login", methods=['POST'])
def login_func():
    data = request.form      #gets data entered by user (email, pw)
    user = User.query.filter_by(email = data['email']).first()    #finds matching entry
    if user and user.check_password(data['password']):
      login_user(user)    #if match found, log user in and redirect to their dashboard page
      return redirect('/dashboard')    
    else:
      flash('Incorrect Email or Password . Retry !!')    #else display error and redirect to login page again
      return redirect('/') 

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)

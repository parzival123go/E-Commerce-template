from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
db = SQLAlchemy()

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)
  is_admin = db.Column(db.Boolean, default=False)
  products = db.relationship('Product', backref=db.backref('users', lazy='joined'))

  def __init__(self, name, email,is_admin, password):
    self.name = name
    self.email = email
    self.is_admin= is_admin
    self.products= []
    self.set_password(password)


     #hashes the password parameter and stores it in the object
  def set_password(self, password):
      """Create hashed password."""
      self.password = generate_password_hash(password, method='pbkdf2:sha256')
  
  #Returns true if the parameter is equal to the object’s password property
  def check_password(self, password):
      """Check hashed password."""
      return check_password_hash(self.password, password)
  
  #To String method
  def __repr__(self):
      return f'<User {self.id}: {self.name}>'  



class Category(db.Model):
  id= db.Column(db.Integer, primary_key=True)
  category_name= db.Column(db.String(80), nullable=False)
  product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

  def __init__(self,name):
    self.category_name = name

    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produt_name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(80))
    expire_date = db.Column(db.Date) 
    expire_date = datetime.strptime("21 March 2019", "%d %B %Y").date()
    units_in_stock = db.Column(db.Integer, nullable=False)
    categories= db.relationship('Category', backref=db.backref('products', lazy='joined'))
   # product_image = db.Column(db.File(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, product_name, description, category, expire_date, units_in_stock):
        self.produt_name = product_name
        self.description = description
        self.category = category
        self.expire_date = expire_date
        self.units_in_stock = units_in_stock
        self.categories=[]


import click
import csv
from App import db, User, Product
from App import app

@app.cli.command("init", help="Creates and initializes the database")
def initialize():
 
  db.drop_all()
  db.create_all()
  bob = User("bob", "bob@mail.com", "bobpass")
  prod =Product(name="product1", description="This is a very nice product", price=200, image_url="https://images.pexels.com/photos/4841375/pexels-photo-4841375.jpeg?auto=compress&cs=tinysrgb&w=600")
  db.session.add(bob)
  db.session.add(prod)
  db.session.commit()
  print("Database intitialized")
  
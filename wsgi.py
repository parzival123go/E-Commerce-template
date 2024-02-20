import click
import csv
from App import db, User, Product
from App import app

@app.cli.command("init", help="Creates and initializes the database")
def initialize():

  db.drop_all()
  db.create_all()
  bob = User("bob", "bob@mail.com",True, "bobpass")
  prod =Product(product_name="product1", description="This is a very nice product", category="Shoes", expire_date="21 March 2019", units_in_stock=10)
  db.session.add(bob)
  db.session.add(prod)
  db.session.commit()
  print("Database intitialized")
  

import click
import csv
from App import db, User
from App import app

@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()
  bob = User("bob", "bob@mail.com", "bobpass")
  db.session.add(bob)
  db.session.commit()
  
  
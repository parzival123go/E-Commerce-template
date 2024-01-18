import os
from flask import Flask, Blueprint, render_template,url_for, redirect, request, flash, make_response, jsonify
from .models import Pokemon, UserPokemon, User, db
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
  app = Flask(__name__, static_url_path='/static')
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['TEMPLATES_AUTO_RELOAD'] = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
  app.config['DEBUG'] = True
  app.config['SECRET_KEY'] = 'MySecretKey'
  app.config['PREFERRED_URL_SCHEME'] = 'https'
  db.init_app(app)
  login_manager.init_app(app)
  login_manager.login_view = "login_page"
  app.app_context().push()
  return app

app = create_app()

#Student ID: 816033508
#Name: Richard Rattansingh

# Page Routes

#To update
@app.route("/", methods=['GET'])   #gets the login page for either route hit
@app.route("/login", methods=['GET'])
def login():
   #return redirect(url_for('home_page'))
  return render_template("login.html")


@app.route("/app", methods=['GET'])
@app.route("/app/<int:pokemon_id>", methods=['GET'])
# add @login_required decorator to require login
@login_required
def home_page(pokemon_id=1):  #by default start with pokemon_id = 1, allows test case 2.2 to pass
    user = current_user   #gets the current user
    
    specific = Pokemon.query.filter_by(id=pokemon_id).first()     #gets the pokemon specified from the url
    pokemon = Pokemon.query.all()   #gets all pokemon to display in sidebar 
    captured = UserPokemon.query.filter_by(user_id=user.id).all()    #gets all captured pokemon with the current user's ID
    return render_template("home.html", pokemon=pokemon, specific=specific, captured=captured)  #pass relevant data to template

@app.route("/logout", methods=['GET'])
@login_required
def logout_action():
  logout_user()      #logs out user and redirects to the main page (login page)
  #flash('Logging Out')
  return redirect('/')  #or '/login'

@app.route("/signup", methods=['GET'])
def signup_action():
  return render_template("signup.html")

@app.route("/signup", methods=['POST'])
def signup_user():
  data = request.form     #gets data entered (username, pw)
  user = User.query.filter_by(username=data['username']).first()      #finds possible matching entry
  if  user:
    flash("username taken, try another")       #if entry exists, display error and redirect to sign up page
    redirect("/signup")
  user = User(username=data['username'], email=data['email'], password=data['password'])
  db.session.add(user)        #else, add user to db and redirect to login
  db.session.commit()
  return redirect("/login")    #could also redirect to the home page but extra work required

# Form Action Routes
@app.route("/login", methods=['POST'])
def login_func():
  data = request.form      #gets data entered by user (username, pw)
  user = User.query.filter_by(username = data['username']).first()    #finds matching entry
  if user and user.check_password(data['password']):
    login_user(user)    #if match found, log user in and redirect to their home page
    return redirect('/app')    
  else:
    flash('something wrong')    #else display error and redirect to login page again
    return redirect('/')  #or /login

@app.route("/pokemon/<int:pokemon_id>", methods=['POST'])
@login_required
def capture_pokemon(pokemon_id):
  flash("capturing pokemon")
  data = request.form       #gets data from selected pokemon form (ID, given name by user)
  pokemon_name = data['pokemon_name']
  user = current_user
  new_pokemon = UserPokemon(user.id, pokemon_id=pokemon_id, name=pokemon_name)   
  db.session.add(new_pokemon)       #adds entry to db, given names don't have to be unique
  db.session.commit()
  return redirect("/app")

@app.route("/release-pokemon/<int:user_poke_id>", methods=['GET'])
@login_required
def release_action(user_poke_id):
  poke = UserPokemon.query.filter_by(id=user_poke_id).first()  #gets entry to be deleted
  if not poke:
    print(f'error deleting')     #if entry does not exist, display error, redirect to home page
    return redirect("/app")
  db.session.delete(poke)
  db.session.commit()
  flash(f'Goodbye {poke.name}')
  return redirect("/app")

@app.route("/rename-pokemon/<int:user_poke_id>", methods=['POST'])
@login_required
def change_name(user_poke_id):
  data = request.form
  poke = UserPokemon.query.filter_by(id=user_poke_id).first()  #gets entry to change name
  if not poke:
    flash("Error changing name")   #if entry does not exist, display error and return
    return
    
  poke.name = data['rename']
  db.session.add(poke)        #else, changes name and commits change to db
  db.session.commit()
  flash("Name changed")
  return redirect("/app")

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)

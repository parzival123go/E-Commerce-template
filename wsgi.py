import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import *
# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    create_user('121', 'bob', 'bobpass')
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

log_review_cli = AppGroup('log_review', help='Log Review object commands')

# Command to test the create_log_review function
@log_review_cli.command("test_create", help="Test create_log_review function")
@click.argument("student_id", type=int)
@click.argument("message")
@click.argument("upvote", type=int, default=0)
@click.argument("downvote", type=int, default=0)
def test_create_review(student_id, message, upvote, downvote):
    log_review_controller = ReviewController()
    result = log_review_controller.create_log_review(student_id, message, upvote, downvote)
    
    if result:
        print(f'Review created successfully:\n{result.to_json()}')  # Print the review object
    else:
        print('Failed to create review.')


# Command to test the search_review function by student ID
@log_review_cli.command("test_search_by_student", help="Test search_review function by student ID")
@click.argument("student_id", type=int)
def test_search_review_by_student(student_id):
    log_review_controller = ReviewController()
    reviews = log_review_controller.search_reviews_by_student(student_id)
    
    if reviews:
        print(f'Reviews found for student ID {student_id}:\n')
        for review in reviews:
            print(f'Review ID: {review["id"]}')
            print(f'Message: {review["message"]}')
            print(f'Upvote: {review["upvote"]}')
            print(f'Downvote: {review["downvote"]}\n')
    else:
        print(f'No reviews found for student ID {student_id}.')




app.cli.add_command(log_review_cli)

'''
Student Commands
'''

# create a group for student commands
student_cli = AppGroup('student', help='Student object commands')

# Command to create a student
@student_cli.command("create", help="Creates a student")
@click.argument("first_name", default="John")
@click.argument("last_name", default="Doe")
@click.argument("email", default="john@example.com")
@click.argument("phone_number", default="123-456-7890")
def create_student_command(first_name, last_name, email, phone_number):
    student_controller = StudentController()
    result = student_controller.create_student(first_name, last_name, email, phone_number)
    
    if result:
        student_name = f'{first_name} {last_name}'  # Concatenate the first and last name
        print(f'Student {student_name} created!')
    else:
        print(f'Failed to create student. Student with the same email may already exist.')

@student_cli.command("update", help="Update student information")
@click.argument("student_id", type=int)
@click.argument("first_name", required=False)
@click.argument("last_name", required=False)
@click.argument("email", required=False)  # Change this to an argument
@click.argument("phone_number", required=False)
def update_student_command(student_id, first_name, last_name, email, phone_number):
    student_controller = StudentController()
    data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone_number': phone_number
    }
    result = student_controller.update_student(student_id, data)
    
    if result:
        print(f'Student with ID {student_id} updated successfully!')
    else:
        print(f'Failed to update student with ID {student_id}. Student not found or update failed.')

@student_cli.command("search", help="Search for a student by ID")
@click.argument("student_id", type=int)
def search_student_command(student_id):
    student_controller = StudentController()
    result = student_controller.search_student(student_id)

    if result:
        print(f'Student found with ID {student_id}:')
        print(result)
    else:
        print(f'Student with ID {student_id} not found.')
        
app.cli.add_command(student_cli)  # add the student group to the CLI

'''
Test Commands (Including Student Tests)
'''

test = AppGroup('test', help='Testing commands')

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

@test.command("student", help="Run Student tests")
@click.argument("type", default="all")
def student_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "StudentUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "StudentIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)
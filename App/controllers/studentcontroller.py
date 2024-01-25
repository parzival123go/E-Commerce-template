# app/controllers/student_controller.py

from App.database import db
from App.models.student import Student

class StudentController:
    # ... Other methods ...

    def create_student(self, first_name, last_name, email, phone_number):
        try:
            # Check if a student with the same email already exists
            existing_student = Student.query.filter_by(email=email).first()

            if existing_student:
                # A student with the same email already exists, return False
                return False

            # Create a new student instance
            new_student = Student(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number
            )

            # Add the new student to the database
            db.session.add(new_student)
            db.session.commit()

            return True  # Student created successfully
        except Exception as e:
            # Handle any exceptions (e.g., database errors) here
            print(str(e))
            db.session.rollback()  # Rollback changes in case of an error
            return False  # Student creation failed

    def update_student(self, student_id, data):
        try:
            # Find the student by ID
            student = Student.query.get(student_id)

            if not student:
                return False  # Student not found

            # Update student data based on the provided data
            if 'first_name' in data:
                student.first_name = data['first_name']
            if 'last_name' in data:
                student.last_name = data['last_name']
            if 'email' in data:
                student.email = data['email']
            if 'phone_number' in data:
                student.phone_number = data['phone_number']

            # Commit the changes to the database
            db.session.commit()

            return True  # Student updated successfully
        except Exception as e:
            # Handle any exceptions (e.g., database errors) here
            print(str(e))
            db.session.rollback()  # Rollback changes in case of an error
            return False  # Student update failed

    def search_student(self, student_id):
        try:
            # Find the student by ID
            student = Student.query.get(student_id)

            if student:
                # Return student information as a dictionary
                student_info = {
                    'student_id': student.id,
                    'first_name': student.first_name,
                    'last_name': student.last_name,
                    'email': student.email,
                    'phone_number': student.phone_number,
                    'karma' : student.karma_score
                }
                return student_info
            else:
                return None  # Student not found
        except Exception as e:
            # Handle any exceptions (e.g., database errors) here
            print(str(e))
            return None  # Search operation failed

    def get_student_by_email(self, email):
        return Student.query.filter_by(email=email).first()

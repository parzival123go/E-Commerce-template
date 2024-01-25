# Import the necessary modules
from App.database import db

class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    message = db.Column(db.String(300), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('user.staff_id'),nullable=False)
 
    def __init__(self, student_id, message,staff_id):
        self.student_id = student_id
        self.message = message
        self.staff_id = staff_id
    
    def to_json(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'message': self.message,
            'staff_id': self.staff_id
        }

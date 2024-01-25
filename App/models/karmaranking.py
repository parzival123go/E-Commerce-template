from App.database import db

class KarmaVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('user.staff_id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)  # 1 for upvote, 0 for downvote

    def __init__(self, staff_id, review_id, value):
        self.staff_id = staff_id
        self.review_id = review_id
        self.value = value

    def get_json(self):
        return {
            'id': self.id,
            'staff_id': self.staff_id,
            'review_id': self.review_id,
            'value': self.value
        }

    def to_json(self):
        return {
            'id': self.id,
            'staff_id': self.staff_id,
            'review_id': self.review_id,
            'value': self.value
        }

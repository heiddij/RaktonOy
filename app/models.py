from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.String(100))
    photo = db.Column(db.LargeBinary)
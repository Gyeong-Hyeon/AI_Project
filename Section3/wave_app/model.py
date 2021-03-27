from wave_app import db

class User(db.Model):
    __tablename__ = 'User'
    
    id = db.Column(db.Integer())
    username = db.Column(db.String(20), nullable=False)
    level = db.Column(db.String(15), nullable=False)

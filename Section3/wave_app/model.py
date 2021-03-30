from wave_app import db

class User(db.Model):
    __tablename__ = 'User'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.Integer, nullable=False)
    level = db.Column(db.String(15), nullable=False)
    waves = db.relationship('Search', backref='User', cascade='all,delete-orphan')

class Search(db.Model):
    __tablename__ = 'Search'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    time = db.Column(db.Integer)
    avg = db.Column(db.Float, nullable=False)
    hg = db.Column(db.Float, nullable=False)
    sec = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))


from flask import Blueprint, request, redirect, url_for
from wave_app import db
from wave_app.model import User

bp = Blueprint('signup', __name__)

@bp.route('/signup', methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if request.form['level'] == '1':
            level = 'Beginner'
        elif request.form['level'] == '2':
            level = 'Intermediate'
        else:
            level = 'Advanced'

        if username and password and level:
            user = db.session.query(User).filter(User.username == username).first()
            if user:
                msg_code=4
            else:
                db.session.add(User(
                    username = username,
                    password = str(password),
                    level = level
                ))
                db.session.commit()
                msg_code=5
        else:
            msg_code=3
    return redirect(url_for('main.signup_index', msg_code=msg_code))


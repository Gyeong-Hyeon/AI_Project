from flask import Blueprint, request, redirect, url_for, render_template
from wave_app import db
from wave_app.model import User, Search

bp = Blueprint('signin', __name__)

@bp.route('/signin', methods=["GET", "POST"])
def index():
    render_template('signin.html')
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        if username and password: #Username을 받으면 DB에 등록된 user인지 조회
            user = db.session.query(User).filter(User.username == username).first()
            if user: #등록된 user이면 password가 맞는지 확인
                if str(password) == user.password: #Password가 맞으면 searchlist에 여태껏 조회했던 list담아서 넘김
                    user_id = user.id  
                    return redirect(url_for('main.user_index', msg_code=0, user_id=user_id))
                else: #Password가 틀릴경우
                    return redirect(url_for('main.fail_index', msg_code=2))
            else: #등록되지 않은 user일 경우
                return redirect(url_for('main.fail_index', msg_code=1))
        else: #Username이나 password가 없을경우
            return redirect(url_for('main.fail_index', msg_code=3))

@bp.route('/signin/<int:user_id>')
def refresh(user_id=None):
    if user_id:
        return redirect(url_for('main.user_index', msg_code=0, user_id=user_id))
    else:
        return render_template('signin.html')


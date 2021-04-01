from flask import Blueprint, render_template, request, redirect, url_for
from wave_app import db
from wave_app.model import User, Search
from wave_app.utils import main_funcs
from datetime import datetime, date, timedelta
import pandas as pd

bp = Blueprint('predict', __name__)

@bp.route('/predict/<int:user_id>', methods=["GET", "POST"])
def predict_target(user_id=None):
    """
    GET 요청: prediction.html 페이지 로드 (users, date 받기)
    POST 요청: prediction 결과값을 딕셔너리 형태로 변수에 담아 prediction.html 페이지에 넘겨줌
    """    
    if user_id:
        user = db.session.query(User).filter(User.id == user_id).first()
        end_date = date.today()+timedelta(days=29)
        cmt = None
        prediction=None
        level=user.level

        if request.method == "POST":
            target_date = request.form['target_date']
            if target_date == '2020-10-09': #시연위해 샘플 만들기
                prediction=[{'time':7,'avg':1.6,'hg':2,'sec':12},{'time':8,'avg':1.8,'hg':2,'sec':12},{'time':9,'avg':1.8,'hg':2,'sec':12}]
            elif target_date == '2020-12-08':
                prediction=[{'time':17,'avg':0.8,'hg':1.0,'sec':10},{'time':18,'avg':0.9,'hg':1.1,'sec':10},{'time':19,'avg':1.0,'hg':1.2,'sec':9}]
            elif target_date == '2020-12-25':
                prediction=[{'time':17,'avg':0.6,'hg':0.65,'sec':7},{'time':18,'avg':0.65,'hg':0.7,'sec':7},{'time':19,'avg':0.7,'hg':0.75,'sec':8}]
            
            #실제 모델
            else:
                dt = datetime.strptime(target_date, '%Y-%m-%d') +timedelta(days=-29) #예측 기준 data는 30일 전 값이므로 30일 전으로 날짜 설정
                dt = str(dt.strftime('%Y-%m-%d'))

                sunrise, sunset = main_funcs.check_sun(dt)
            
                #target date feature정보 크롤링
                starttime = int(sunrise)+2
                endtime = int(sunset)
                data_1 = main_funcs.make_X(dt,starttime,starttime+9)
                data_2 = main_funcs.make_X(dt,starttime+10,endtime)
                for row in data_2:
                    data_1.append(row)
                df = pd.DataFrame(data_1)
                df = df.apply(pd.to_numeric)
                
                #모델돌리기
                avg = main_funcs.predict_avg(df)
                hgst = main_funcs.predict_hgst(df)
                sec = main_funcs.predict_sec(df)

                prediction=[]
                for i in range(len(avg)):
                    prediction.append({
                        'time':int(sunrise)+1+i,
                        'avg':round(avg[i],2),
                        'hg':round(hgst[i],2),
                        'sec':round(sec[i],2)
                    })

            cmt, searches = main_funcs.check_condition(prediction, level, target_date)

            for raw in searches:
                db.session.add(Search(
                    date=target_date,
                    time=raw['time'],
                    avg=raw['avg'],
                    hg=raw['hg'],
                    sec=raw['sec'],
                    user_id=user_id
                ))
                db.session.commit()

        return redirect(url_for('main.predict_index', user_id=user_id, name=user.username, level=level, end_date=end_date, msg=cmt, prediction=prediction))
    else:
        return 'Please sign in first'
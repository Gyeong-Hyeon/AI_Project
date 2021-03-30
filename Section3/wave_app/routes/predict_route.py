from flask import Blueprint, render_template, request, redirect, url_for
from wave_app import db
from wave_app.model import User, Search
from wave_app.utils import main_funcs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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

        if request.method == "POST":
            target_date = request.form['target_date']
            dt = datetime.strptime(target_date, '%Y-%m-%d') +timedelta(days=-29) #예측 기준 data는 30일 전 값이므로 30일 전으로 날짜 설정
            dt = str(dt.strftime('%Y-%m-%d'))

            #일출, 일몰시간 크롤링
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='C:/Users/user/Desktop/chromedriver.exe')

            url = f'https://astro.kasi.re.kr/life/pageView/9?lat=33.24487748986555&lng=126.40578906148072&date={dt}&address=제주특별자치도+서귀포시+중문관광로72번길+114'
            driver.get(url)
            sunrise = BeautifulSoup(driver.page_source, 'html.parser').find_all('span', {'class': 'sunrise'})[0].string.split('시')[0]
            sunset = BeautifulSoup(driver.page_source, 'html.parser').find_all('span', {'class': 'sunset'})[0].string.split('시')[0]
           
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
                    'avg':avg[i],
                    'hg':hgst[i],
                    'sec':sec[i]
                })
            
            level = user.level
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
            
            breakpoint()
        return redirect(url_for('main.predict_index', user_id=user_id, name=user.username, level=level, end_date=end_date, msg=cmt, prediction=prediction))
    else:
        return 'Please sign in first'
from flask import Blueprint, render_template, request
from wave_app.utils import main_funcs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/prediction', methods=["GET", "POST"])
def compare_index():
    """
    GET 요청: prediction.html 페이지 로드 (users, date 받기)
    POST 요청: prediction 결과값을 딕셔너리 형태로 변수에 담아 prediction.html 페이지에 넘겨줌
    """
    users = 
    prediction = None

    if request.method == "POST":
        target_date = reqeust.form['target_date']
        date = datetime.strptime(target_date, '%Y-%m-%d') - 30 #예측 기준 data는 30일 전 값이므로 30일 전으로 날짜 설정

        #일출, 일몰시간 크롤링
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='C:/Users/user/Desktop/chromedriver.exe')

        url = f'https://astro.kasi.re.kr/life/pageView/9?lat=33.24487748986555&lng=126.40578906148072&date={date}&address=제주특별자치도+서귀포시+중문관광로72번길+114'
        driver.get(url)
        sunrise = BeautifulSoup(driver.page_source, 'html.parser').find_all('span', {'class': 'sunrise'})[0].string.split('시')[0]
        sunset = BeautifulSoup(driver.page_source, 'html.parser').find_all('span', {'class': 'sunset'})[0].string.split('시')[0]

        sunrise = int(sunrise)
        sunset = int(sunset)

        #일출 1시간 이후~일몰 1시간 전 사이 1시간 주기 예측값 낼 X_test 크롤링

        for time in range(sunrise+1,sunset):
            






         
    return render_template('prediction.html', prediction=prediction)

@bp.route('/user')
def user_index():
    """
    데이터베이스에 있는 user_list 에 유저들을 담아 user.html 파일에 전달
    """

    msg_code = request.args.get('msg_code', None)
    
    alert_msg = main_funcs.msg_processor(msg_code) if msg_code is not None else None

    user_list = None

    return render_template('user.html', alert_msg=alert_msg, user_list=user_list)
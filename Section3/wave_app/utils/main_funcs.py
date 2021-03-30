'''
파도높이, 파주기, 풍향 예측 모델
- Random forest 모델 사용, Randomized search 및 Grid search로 모델 튜닝 (자세한 과정은 ipynb파일 확인)
- 자료 출처: 기상청
- 현재 우라나라 시각별 남부 및 동부 해안 풍속, 풍향, 기압, 습도, 기온, 수온, 최대*유의*평균파고, 파주기, 파향을 기반으로 30일 후 동일 시각의
파도높이, 파주기, 풍향 예측하여 서핑에 적합한 파도 높이/파주기/ 풍향인지 확인

- 파도 높이 구분
 * 패들 연습: 0.3m ~ 0.4m
 * Beginner: 0.5m ~ 0.7m
 * Intermediate: 0.7m ~ 1.5m
 * Advanced: 1.5m ~ 2m

- 파주기 구분
 * 패들 연습: 6초 이하
 * 좋은 파도: 6초 초과
'''

import joblib
import time
import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

def make_X(date,starttime,endtime):
    url = 'https://data.kma.go.kr/data/sea/selectBuoyRltmList.do?pgmNo=52'

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='C:/Users/user/Desktop/chromedriver.exe')
    driver.get(url=url)
    time.sleep(1)

    startdate = driver.find_element_by_xpath('//*[@id="startDt_d"]')
    startdate.clear()
    startdate.send_keys(date)

    driver.find_element_by_xpath(f'//*[@id="startHh"]/option[{starttime}]').click()

    enddate = driver.find_element_by_xpath('//*[@id="endDt_d"]')
    enddate.clear()
    enddate.send_keys(date)

    driver.find_element_by_xpath(f'//*[@id="endHh"]/option[{endtime}]').click()

    driver.find_element_by_xpath('//*[@id="ztree_2_switch"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="ztree_9_check"]').click()
    driver.find_element_by_xpath('//*[@id="ztree1_1_check"]').click()

    driver.find_element_by_xpath('//*[@id="dsForm"]/div[3]/button').click()
    time.sleep(1)

    tbody = driver.find_element_by_xpath('//*[@id="contentsList"]')
    tr = tbody.find_elements_by_tag_name('tr')

    data = []
    for td in tr:
        row_list = td.text.split()
        month = row_list[1].split('-')[1]
        day = row_list[1].split('-')[2]
        hour = row_list[2].split(':')[0]
        row_list[0]=int(month)
        row_list[1]=int(day)
        row_list[2]=int(hour)
        data.append(row_list)

    return data

def predict_avg(X_test):
    model = joblib.load('md_a.pkl')
    predict = model.predict(X_test)
    return predict

def predict_hgst(X_test):
    model = joblib.load('md_h.pkl')
    predict = model.predict(X_test)
    return predict

def predict_sec(X_test):
    model = joblib.load('md_s.pkl')
    predict = model.predict(X_test)
    return predict

def check_condition(prediction, level):
    #레벨별로 파도 나누기
    beg =[]
    inter = []
    adv = []
    for raw in prediction:
        if raw['sec'] >6 and raw['avg'] > 0.5:
            if raw['avg'] > 1.5:
                adv.append(raw)
            elif raw['avg']  > 0.7:
                inter.append(raw)
            else:
                beg.append(raw)
        else:
            pass
    #레벨별로 메세지 구분
    if level == 'Advanced':
        searches = adv
        if len(adv)==0 and len(inter)==0:
            msg = f"{target_date}는 서핑하기엔 파도 condition이 좋지 않아요 :( 다른 날은 어때요?"
        elif len(adv)==0 and len(inter)!=0:
            for raw in inter:
                times.append(raw['time'])
            msg = f"{target_date}는 중급자 수준의 파도가 치는 날이라 조금 낮을 수 있어요 :( 만약 탄다면 {','.join(str(e) for e in times)}시 정도 추천?"
        elif len(adv)!=0:
            for raw in adv:
                times.append(raw['time'])
            msg = f"{target_date}의 {','.join(str(e) for e in times)}시에는 서핑하기 좋을 것 같아요 :)"
        
    elif level == 'Intermediate':
        searches = inter
        if len(adv)==0 and len(inter)==0:
            msg = f"{target_date}는 서핑하기엔 파도 condition이 좋지 않아요 :( 다른 날은 어때요?"
        elif len(adv)!=0 and len(inter)==0:
            for raw in adv:
                times.append(raw['time'])
            msg = f"{target_date}는 숙련자 수준의 파도가 치는 날이라 위험할 수 있어요!! 조심해서 {','.join(str(e) for e in times)}시 정도를 노려보세요"
        elif len(beg)!=0 and len(inter)==0:
            for raw in beg:
                times.append(raw['time'])
            msg = f"{target_date}는 초급자 수준의 파도가 치는 날이라 조금 낮을 수 있어요 :( 만약 탄다면 {','.join(str(e) for e in times)}시 정도 추천?"
        elif len(inter)!=0:
            for raw in inter:
                times.append(raw['time'])
            msg = f"{target_date}의 {','.join(str(e) for e in times)}시에는 서핑하기 좋을 것 같아요 :)"
   
    else:
        searches = beginner
        if len(inter)!=0 or len(adv) !=0:
            msg = f"{target_date}는 파도가 너무 높아서 초급자에게는 위험해요. 다른 날 도전해봐요!"
        elif len(beg)==0:
            msg = f"{target_date}는 서핑하기엔 파도가 좋지 않네요. 대신 패들 연습 어때요?"
        elif len(beg)!=0:
            for raw in beg:
                times.append(raw['time'])
            msg = f"{target_date}의 {','.join(str(e) for e in times)}시에는 서핑하기 좋을 것 같아요 :)"

    return msg, searches



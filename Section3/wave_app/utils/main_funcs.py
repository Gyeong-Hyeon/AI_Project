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

from sklearn.externals import joblib

def make_x():



def predict_avg(X_test):
    model = joblib.load()
    predict = model.predict(X_test)
    return 

def predict_hgst(X_test):
    model = joblib.load()
    predict = model.predict(X_test)

def predict_sec(X_test):
    model = joblib.load()
    predict = model.predict(X_test)

from flask import Flask  # 서버 구현을 위한 Flask 객체 import
from flask import request, jsonify
import requests

WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/"
WEARTHER_SEC_KEY = "Your API Key"
IP_TRACKING_API_URL = "http://api.ipstack.com/"
IP_TRACKING_KEY = "Your API Key"
GET_GMTPLUS_TIME = "http://worldtimeapi.org/api/timezone/"

app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.

@app.route('/weatherInterface')  # 데코레이터 이용, '/weatherInterface' 경로에 클래스 등록
def get():  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
    clientIp = request.remote_addr
    #IP 가공 로컬아이피 대체하기
    clientIp = "Your PC IP"

    #ip로 주소얻어오기
    targetUrl = IP_TRACKING_API_URL + clientIp + "?access_key=" + IP_TRACKING_KEY
    response = requests.get(targetUrl)
    print(response.json())
    regionName = response.json()['region_name']
    continent_name = response.json()['continent_name']
    regionName = "Seoul" # IP 고정으로 인한 특수처리

    #지역으로 날씨 얻어오기
    targetUrl = WEATHER_API_URL + "weather?q=" + regionName + "&appid=" + WEARTHER_SEC_KEY
    response = requests.get(targetUrl)
    #json 데이터 구조파악
    weather = response.json()['weather'][0]['main']
    print("weather : " + weather)

    #GMT표준시간 구하기
    targetUrl = GET_GMTPLUS_TIME + continent_name + "/" + regionName
    response = requests.get(targetUrl)
    plusTime = response.json()['raw_offset']
    print(plusTime)

    #구조잡아서 리턴
    result = []
    result.append(["regionname", regionName])
    result.append(["time", plusTime])
    result.append(["weather", weather])
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
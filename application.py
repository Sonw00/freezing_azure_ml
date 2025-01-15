from flask import Flask, render_template, request, jsonify
import requests
from collections import defaultdict

app = Flask(__name__)

# 기상청 API 설정
SERVICE_KEY = "u/tFOWu9xDYgBc2n6zUlZ+6PpZ3tLIUrjTcPxNnHPWQE8y4w2XzU3fHUre1ZEyB9hzPSDgN+KIEqIHB4U16Y6w=="  # 발급받은 서비스 키 입력
BASE_URL = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
DATA_TYPE = "JSON"  # 요청 데이터 형식

# 지역별 nx, ny 좌표 설정
LOCATION_COORDS = {
    "경기도": {
        "화성시": {"nx": 57, "ny": 119, "위도":37.196816, "경도":126.833530},
        "수원시": {"nx": 60, "ny": 121, "위도":37.301011, "경도":127.012222},
        "성남시": {"nx": 63, "ny": 124, "위도":37.447491, "경도":127.147719},
        "의정부시": {"nx": 61, "ny": 130, "위도":37.735288, "경도":127.035841},
        "안양시": {"nx": 59, "ny": 123, "위도":37.383777, "경도":126.934500},
        "부천시": {"nx": 57, "ny": 125, "위도":37.496592, "경도":126.786997},
        "광명시": {"nx": 58, "ny": 125, "위도":37.475750, "경도":126.866708},
        "평택시": {"nx": 62, "ny": 114, "위도":36.989438, "경도":127.114655},
        "동두천시": {"nx": 61, "ny": 134, "위도":37.900916, "경도":127.062652},
        "안산시": {"nx": 58, "ny": 121, "위도":37.298519, "경도":126.846819},
        "고양시": {"nx": 57, "ny": 128, "위도":37.634583, "경도":126.834197},
        "과천시": {"nx": 60, "ny": 124, "위도":37.4263722, "경도":126.9898},
        "구리시": {"nx": 62, "ny": 127, "위도":37.591625, "경도":127.131863},
        "남양주시": {"nx": 64, "ny": 128, "위도":37.633177, "경도":127.218633},
        "오산시": {"nx": 62, "ny": 118, "위도":37.146913, "경도":127.079641},
        "시흥시": {"nx": 57, "ny": 123, "위도":37.377319, "경도":126.805077},
        "군포시": {"nx": 59, "ny": 122, "위도":37.358658, "경도":126.9375},
        "의왕시": {"nx": 60, "ny": 122, "위도":37.34195, "경도":126.970388},
        "하남시": {"nx": 64, "ny": 126, "위도":37.536497, "경도":127.217},
        "용인시": {"nx": 64, "ny": 119, "위도":37.231477, "경도":127.203844},
        "파주시": {"nx": 56, "ny": 131, "위도":37.757083, "경도":126.781952},
        "이천시": {"nx": 68, "ny": 121, "위도":37.275436, "경도":127.443219},
        "안성시": {"nx": 65, "ny": 115, "위도":37.005175, "경도":127.28184},
        "김포시": {"nx": 55, "ny": 128, "위도":37.612458, "경도":126.717777},
        "광주시": {"nx": 65, "ny": 123, "위도":37.414505, "경도":127.257786},
        "양주시": {"nx": 61, "ny": 131, "위도":37.78245, "경도":127.04781},
        "포천시": {"nx": 64, "ny": 134, "위도":37.892155, "경도":127.20241},
        "여주시": {"nx": 71, "ny": 121, "위도":37.295358, "경도":127.639622},
        "연천군": {"nx": 61, "ny": 138, "위도":38.093363, "경도":127.077066},
        "가평군": {"nx": 69, "ny": 133, "위도":37.828830, "경도":127.511777},
        "양평군": {"nx": 69, "ny": 125, "위도":37.488936, "경도":127.489886},
    },
    "서울특별시": {
        "--": {"nx": 60, "ny": 127, "위도":126.980008, "경도":37.563569},
    },
    "인천광역시": {
        "--": {"nx": 55, "ny": 124, "위도":126.707352, "경도":	37.453233},
    },
}

@app.route('/')
def index():
    return render_template('index.html', locations=LOCATION_COORDS)

@app.route('/get_weather', methods=['POST'])
def get_weather():
    data = request.json
    region = data.get("region")
    city = data.get("city")
    
    if region not in LOCATION_COORDS or city not in LOCATION_COORDS[region]:
        return jsonify({"error": "Invalid region or city"}), 400
    
    # 선택한 지역의 nx, ny 값 가져오기
    coords = LOCATION_COORDS[region][city]
    nx, ny = coords["nx"], coords["ny"]

    # 요청 파라미터 설정
    params = {
        "serviceKey": SERVICE_KEY,
        "numOfRows": 1000,
        "pageNo": 1,
        "dataType": DATA_TYPE,
        "base_date": "20250115",  # 예시로 오늘 날짜 사용
        "base_time": "0500",
        "nx": nx,
        "ny": ny,
    }

    # API 호출
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        result = response.json()
        if result.get("response", {}).get("header", {}).get("resultCode") == "00":
            items = result["response"]["body"]["items"]["item"]
            
            # 날짜와 시간별 데이터를 저장할 딕셔너리
            weather_data = defaultdict(lambda: defaultdict(dict))
            for item in items:
                date = item["fcstDate"]
                time = item["fcstTime"]
                category = item["category"]
                value = item["fcstValue"]
                weather_data[date][time][category] = value
            
            return jsonify(weather_data)
        else:
            return jsonify({"error": "API response error"}), 500
    else:
        return jsonify({"error": "Failed to fetch weather data"}), 500

if __name__ == '__main__':
    app.run(debug=True)

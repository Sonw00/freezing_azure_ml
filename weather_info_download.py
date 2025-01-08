import requests  # requests 모듈 임포트


def download_file(file_url, save_path):
    try:
        response = requests.get(file_url)
        if response.status_code == 200:
            print(f"응답 내용: {response.text}") #데이터 확인용
            #with open(save_path, 'wb') as f:  # 바이너리 쓰기 모드로 파일 열기
            #    f.write(response.content)
            print("파일 다운로드 성공!")
        else:
            print(f"다운로드 실패! 상태 코드: {response.status_code}")
            print(f"응답 내용: {response.text}")
    except Exception as e:
        print(f"오류 발생: {e}")


# URL과 저장 경로 설정
stations = [98] #관측지점정보
stn_param = ",".join(map(str, stations))
tm1 = 202401310000 #기간검색 시작날
tm2 = 202401312300 #기간검색 마지막날
url = f'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm3.php?tm1={tm1}&tm2={tm2}&stn={stn_param}&help=1&authKey=CH8XAAZ1Qxq_FwAGdcMa8w'

print(url)
save_file_path = 'weather2402_g_d.csv'   #저장할 파일명 설정

# 파일 다운로드 실행
download_file(url, save_file_path)
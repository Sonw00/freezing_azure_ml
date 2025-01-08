import requests  # requests 모듈 임포트

def download_file(file_url, save_path):
    try:
        response = requests.get(file_url)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:  # 바이너리 쓰기 모드로 파일 열기
                f.write(response.content)
            print("파일 다운로드 성공!")
        else:
            print(f"다운로드 실패! 상태 코드: {response.status_code}")
            print(f"응답 내용: {response.text}")
    except Exception as e:
        print(f"오류 발생: {e}")

# URL과 저장 경로 설정
url = 'https://apihub.kma.go.kr/api/typ01/url/kma_sfcdd3.php?tm1=20230101&tm2=20230228&help=1&authKey=PdBws84lTJyQcLPOJfycOA'
save_file_path = 'weather_file3.csv'

# 파일 다운로드 실행
download_file(url, save_file_path)

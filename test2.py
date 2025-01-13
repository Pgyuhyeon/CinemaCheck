import json
import requests
from datetime import datetime
import sys

# 오늘 날짜를 자동 설정
def get_today_date():
    return datetime.now().strftime("%Y-%m-%d")

# 원본 JSON 파일 저장 함수
def save_raw_json(data, cinema_name):
    # 영화관 이름에서 공백 및 특수 문자 제거
    safe_cinema_name = "".join(c for c in cinema_name if c.isalnum() or c == "_")
    output_filename = f"{safe_cinema_name}_raw_data.json"

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"원본 데이터를 {output_filename} 파일로 저장했습니다.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <cinema_name> <cinema_code>")
        sys.exit(1)

    cinema_name = sys.argv[1]  # 영화관 이름 (JSON 파일 이름으로 사용)
    cinema_code = sys.argv[2]  # 영화관 코드

    # API 요청 설정
    url = "https://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx"
    today_date = get_today_date()

    param_list = json.dumps({
        "MethodName": "GetPlaySequence",
        "channelType": "HO",
        "osType": "W",
        "osVersion": "Mozilla/5.0",
        "playDate": today_date,
        "cinemaID": cinema_code,
        "representationMovieCode": ""
    })

    files = {"paramList": (None, param_list)}
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.lottecinema.co.kr",
        "Referer": "https://www.lottecinema.co.kr/NLCHS/Ticketing/Schedule"
    }

    response = requests.post(url, files=files, headers=headers)

    if response.status_code == 200:
        response_data = response.json()

        # 원본 JSON 저장
        save_raw_json(response_data, cinema_name)
    else:
        print(f"API 요청 실패: {response.status_code}")

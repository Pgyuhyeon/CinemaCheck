import pymongo
import json
import requests
from datetime import datetime, timedelta
import sys

# MongoDB 연결 설정
client = pymongo.MongoClient("mongodb://localhost:27017/")

# 오늘 날짜를 자동 설정
def get_today_date():
    return datetime.now().strftime("%Y-%m-%d")

# 날짜 정보가 없는 기존 데이터 삭제
def delete_old_data(cinema_name):
    safe_cinema_name = "".join(c for c in cinema_name if c.isalnum() or c == "_")
    db = client[safe_cinema_name]
    collection = db["Movies"]
    result = collection.delete_many({"Date": {"$exists": False}})
    print(f"{safe_cinema_name} 데이터베이스에서 {result.deleted_count}개의 날짜 정보가 없는 데이터를 삭제했습니다.")

# StartTime이 null이 아닌 데이터만 추출하여 MongoDB에 저장하는 함수
def filter_and_save_data(data, cinema_name, date):
    # 영화관 이름에서 공백 및 특수 문자 제거
    safe_cinema_name = "".join(c for c in cinema_name if c.isalnum() or c == "_")

    play_sequences = data.get("PlaySeqs", {}).get("Items", [])
    
    extracted_data = []
    for item in play_sequences:
        start_time = item.get("StartTime")

        # StartTime이 null이거나 비어있는 데이터는 제외
        if not start_time:
            continue

        # 데이터 추출
        movie_name = item.get("MovieNameKR", "N/A")
        screen_name = item.get("ScreenNameKR", "N/A")
        total_seats = item.get("TotalSeatCount", 0)
        booking_seats = item.get("BookingSeatCount", 0)

        # 데이터 구조 생성
        movie_info = {
            "CinemaName": cinema_name.replace(" ", ""),  # 영화관 이름 추가
            "MovieName": movie_name,
            "StartTime": start_time,
            "ScreenName": screen_name,
            "BookingSeatCount": booking_seats,
            "TotalSeatCount": total_seats,
            "Date": date  # 상영 날짜 추가
        }
        extracted_data.append(movie_info)

    # MongoDB 저장
    db = client[safe_cinema_name]
    collection = db["Movies"]
    if extracted_data:
        collection.insert_many(extracted_data)
        print(f"{safe_cinema_name} 데이터베이스에 {len(extracted_data)}개의 데이터를 저장했습니다.")
    else:
        print(f"{safe_cinema_name} 데이터베이스에 저장할 데이터가 없습니다.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <cinema_name> <cinema_code>")
        sys.exit(1)

    cinema_name = sys.argv[1]  # 영화관 이름 (데이터베이스 이름 및 JSON 파일 이름으로 사용)
    cinema_code = sys.argv[2]  # 영화관 코드

    # 날짜 정보가 없는 기존 데이터 삭제
    delete_old_data(cinema_name)

    # API 요청 설정
    url = "https://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx"
    today = datetime.now()
    dates = [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(3)]  # 오늘부터 3일간의 날짜

    for date in dates:
        param_list = json.dumps({
            "MethodName": "GetPlaySequence",
            "channelType": "HO",
            "osType": "W",
            "osVersion": "Mozilla/5.0",
            "playDate": date,
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
            filter_and_save_data(response_data, cinema_name, date)
        else:
            print(f"API 요청 실패: {response.status_code}")

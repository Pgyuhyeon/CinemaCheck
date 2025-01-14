import sys
import requests
import json
from datetime import datetime
from pymongo import MongoClient

def get_today_date():
    """현재 날짜를 YYYYMMDD 형식으로 반환"""
    return datetime.now().strftime("%Y%m%d")

def clean_cinema_name(cinema_name):
    """영화관 이름에서 확장자나 불필요한 부분 제거"""
    return cinema_name.replace(".json", "").replace(".", "").replace("_schedule", "")

def crawl_megabox_schedule(theater_code, cinema_name):
    """메가박스 영화 상영 정보를 크롤링하고 MongoDB에 저장하는 함수"""
    url = "https://megabox.co.kr/on/oh/ohc/Brch/schedulePage.do"
    payload = {
        "masterType": "brch",
        "detailType": "area",
        "brchNo": theater_code,
        "brchNo1": theater_code,
        "firstAt": "Y",
        "playDe": get_today_date(),
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Referer": "https://megabox.co.kr/booking/timetable",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Type": "application/json; charset=UTF-8",
    }

    try:
        # MongoDB 연결
        client = MongoClient("mongodb://localhost:27017/")
        clean_name = clean_cinema_name(cinema_name)  # 이름 정리
        db = client[clean_name]
        collection = db["Movies"]

        # POST 요청 보내기
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            movie_list = data.get("megaMap", {}).get("movieFormList", [])
            today_date = get_today_date()

            # 필요한 정보만 추출 및 현재 날짜 추가
            filtered_movies = [
                {
                    "CinemaName": clean_name,
                    "MovieName": movie.get("movieNm", "N/A"),
                    "StartTime": movie.get("playStartTime", "N/A"),
                    "ScreenName": movie.get("theabExpoNm", "N/A"),
                    "BookingSeatCount": movie.get("restSeatCnt", 0),
                    "TotalSeatCount": movie.get("totSeatCnt", 0),
                    "Date": today_date  # 현재 날짜 추가
                }
                for movie in movie_list
            ]

            # MongoDB에 저장
            collection.delete_many({})  # 기존 데이터 삭제
            if filtered_movies:
                collection.insert_many(filtered_movies)
                print(f"Successfully saved schedule data for {clean_name} to MongoDB database '{clean_name}'")
            else:
                print("No movies found in the response.")
        else:
            print(f"Failed to retrieve data for {cinema_name}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred while crawling {cinema_name}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <theater_code> <cinema_name>")
        sys.exit(1)

    theater_code = sys.argv[1]
    cinema_name = sys.argv[2]

    print(f"Crawling schedule for {cinema_name} (Theater Code: {theater_code}) on {get_today_date()}...")
    crawl_megabox_schedule(theater_code, cinema_name)

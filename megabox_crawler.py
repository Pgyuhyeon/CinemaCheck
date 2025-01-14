import sys
import requests
import json
from datetime import datetime, timedelta
from pymongo import MongoClient
import html  # HTML 디코딩을 위한 모듈 추가

def get_today_date():
    """현재 날짜를 YYYYMMDD 형식으로 반환"""
    return datetime.now().strftime("%Y%m%d")

def clean_cinema_name(cinema_name):
    """영화관 이름에서 확장자나 불필요한 부분 제거"""
    return cinema_name.replace(".json", "").replace(".", "").replace("_schedule", "")

def crawl_megabox_schedule(theater_code, cinema_name):
    """메가박스 영화 상영 정보를 크롤링하고 MongoDB에 저장하는 함수"""
    client = MongoClient("mongodb://localhost:27017/")
    clean_name = clean_cinema_name(cinema_name)  # 이름 정리
    db = client[clean_name]
    collection = db["Movies"]

    today = datetime.now()
    dates = [(today + timedelta(days=i)).strftime("%Y%m%d") for i in range(3)]  # 오늘부터 3일치 날짜

    # 날짜가 없는 기존 데이터 삭제
    collection.delete_many({"Date": {"$exists": False}})

    all_filtered_movies = []

    for date in dates:
        url = "https://megabox.co.kr/on/oh/ohc/Brch/schedulePage.do"
        payload = {
            "masterType": "brch",
            "detailType": "area",
            "brchNo": theater_code,
            "brchNo1": theater_code,
            "firstAt": "Y",
            "playDe": date,
        }
# Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36

        headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "127",
    "Content-Type": "application/json; charset=UTF-8",
    "Host": "www.megabox.co.kr",
    "Origin": "https://www.megabox.co.kr",
    "Pragma": "no-cache",
    "Referer": "https://www.megabox.co.kr/booking/timetable",
    "Sec-CH-UA": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": "\"macOS\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                movie_list = data.get("megaMap", {}).get("movieFormList", [])

                filtered_movies = [
                    {
                        # CinemaName에도 HTML 디코딩 추가
                        "CinemaName": html.unescape(clean_name),
                        "MovieName": movie.get("movieNm", "N/A"),
                        "StartTime": movie.get("playStartTime", "N/A"),
                        # HTML 엔티티를 디코딩
                        "ScreenName": html.unescape(movie.get("theabExpoNm", "N/A")),
                        "BookingSeatCount": movie.get("restSeatCnt", 0),
                        "TotalSeatCount": movie.get("totSeatCnt", 0),
                        "Date": date  # 상영 날짜 추가
                    }
                    for movie in movie_list
                ]

                all_filtered_movies.extend(filtered_movies)
            else:
                print(f"Failed to retrieve data for {cinema_name} on {date}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error occurred while crawling {cinema_name} on {date}: {str(e)}")

    if all_filtered_movies:
        collection.insert_many(all_filtered_movies)
        print(f"Successfully saved schedule data for {clean_name} to MongoDB database '{clean_name}'")
    else:
        print("No movies found in the response.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <theater_code> <cinema_name>")
        sys.exit(1)

    theater_code = sys.argv[1]
    cinema_name = sys.argv[2]

    print(f"Crawling schedule for {cinema_name} (Theater Code: {theater_code}) for the next 3 days...")
    crawl_megabox_schedule(theater_code, cinema_name)

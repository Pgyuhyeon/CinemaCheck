import sys
import requests
from bs4 import BeautifulSoup
import pymongo
from datetime import datetime, timedelta
import time  # 요청 간 지연 추가를 위한 모듈
import re

# MongoDB 연결 설정
client = pymongo.MongoClient("mongodb://localhost:27017/")

def get_today_date():
    """현재 날짜를 YYYYMMDD 형식으로 반환"""
    return datetime.now().strftime("%Y%m%d")

def crawl_and_save_cgv_schedule(region_code, theater_code, cinema_name):
    """CGV 영화관 데이터를 크롤링하고 MongoDB에 저장"""
    today = datetime.now()
    dates = [(today + timedelta(days=i)).strftime("%Y%m%d") for i in range(3)]  # 오늘부터 3일치 날짜

    # MongoDB 컬렉션 설정
    theater_db = client[cinema_name.replace(" ", "_")]
    collection = theater_db["Movies"]

    # 현재 날짜가 지난 데이터 삭제
    collection.delete_many({"Date": {"$lt": get_today_date()}})

    # 날짜가 없는 데이터 삭제
    collection.delete_many({"Date": {"$exists": False}})

    for date in dates:
        # CGV 상영 정보 URL
        url = f"http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode={region_code}&theatercode={theater_code}&date={date}"

        # 요청 헤더 설정
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0 Safari/537.36",
            "Referer": f"http://www.cgv.co.kr/theaters/?theaterCode={theater_code}",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Cookie": "ASP.NET_SessionId=bpt2pknx2uniltzutbfqswdd; WMONID=sD_d1DmK6Lf;"
        }

        # 요청 보내기
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"{date} 요청 실패: {e}")
            continue

        # HTML 파싱
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        # 영화 정보 추출
        movie_li_list = soup.select("div.sect-showtimes > ul > li")

        for li in movie_li_list:
            col_times = li.select_one("div.col-times")
            if not col_times:
                continue

            # 영화 제목 추출
            info_movie = col_times.select_one("div.info-movie")
            movie_title = (
                info_movie.select_one("strong").get_text(strip=True)
                if info_movie and info_movie.select_one("strong")
                else "N/A"
            )

            # 상영관 정보와 시간표 추출
            type_hall_list = col_times.select("div.type-hall")
            for hall in type_hall_list:
                info_hall = hall.select_one("div.info-hall ul")
                hall_name = (
                    info_hall.select("li")[1].get_text(strip=True)
                    if info_hall and len(info_hall.select("li")) >= 2
                    else "N/A"
                )
                total_seat = (
                    re.sub(r"[^0-9]", "", info_hall.select("li")[2].get_text(strip=True))
                    if info_hall and len(info_hall.select("li")) >= 3
                    else 0
                )

                time_table = hall.select_one("div.info-timetable ul")
                if not time_table:
                    continue

                a_tags = time_table.select("li > a")
                for a_tag in a_tags:
                    start_time = a_tag.select_one("em").get_text(strip=True) if a_tag.select_one("em") else None
                    seat_remain = a_tag.get("data-seatremaincnt")

                    movie_info = {
                        "CinemaName": cinema_name,
                        "MovieName": movie_title,
                        "StartTime": start_time,
                        "ScreenName": hall_name,
                        "BookingSeatCount": seat_remain,
                        "TotalSeatCount": total_seat,
                        "Date": date  # 상영 날짜 추가
                    }

                    # 중복 방지를 위해 MongoDB 업데이트
                    collection.update_one(
                        {
                            "CinemaName": cinema_name,
                            "MovieName": movie_title,
                            "StartTime": start_time,
                            "ScreenName": hall_name,
                            "Date": date
                        },
                        {"$set": movie_info},  # 데이터 업데이트
                        upsert=True  # 데이터가 없으면 삽입
                    )

       

    print(f"{cinema_name} 데이터 크롤링 완료.")

if __name__ == "__main__":
    # 커맨드라인 인자 처리
    if len(sys.argv) < 4:
        print("Usage: python script.py <region_code> <theater_code> <cinema_name>")
        sys.exit(1)

    region_code = sys.argv[1]
    theater_code = sys.argv[2]
    cinema_name = sys.argv[3]

    print(f"{cinema_name} 데이터 크롤링 시작...")
    crawl_and_save_cgv_schedule(region_code, theater_code, cinema_name)

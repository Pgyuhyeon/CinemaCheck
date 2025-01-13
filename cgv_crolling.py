import requests
from bs4 import BeautifulSoup
import re

def crawl_cgv_schedule():
    url = "http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=206,04,06&theatercode=0295&date=20250111"

    # 여기서 개발자 도구(Network 탭)나 Postman에서 확인한 헤더들을 그대로 포함
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Referer": "http://www.cgv.co.kr/theaters/?areacode=206%2c04%2c06&theaterCode=0295",
        "Cookie": "ASP.NET_SessionId=w5gmdacdsgpsvkqa2zukccdl; WMONID=D35FvTIM8SI; ...", 
        # ↑ 실제로 본인이 받은 쿠키 문자열 전체를 복사해서 붙여넣기
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                  "image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"요청 실패: {response.status_code}")
        return []

    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    movie_li_list = soup.select("div.sect-showtimes > ul > li")
    results = []

    for li in movie_li_list:
        col_times = li.select_one("div.col-times")
        if not col_times:
            continue

        info_movie = col_times.select_one("div.info-movie")
        if info_movie:
            title_tag = info_movie.select_one("strong")
            movie_title = title_tag.get_text(strip=True) if title_tag else None
        else:
            movie_title = None

        type_hall_list = col_times.select("div.type-hall")
        for hall in type_hall_list:
            info_hall = hall.select_one("div.info-hall ul")
            if info_hall:
                hall_li = info_hall.select("li")
                hall_format = hall_li[0].get_text(strip=True) if len(hall_li) >= 1 else None
                hall_name   = hall_li[1].get_text(strip=True) if len(hall_li) >= 2 else None
                total_seat_text = hall_li[2].get_text(strip=True) if len(hall_li) >= 3 else None

                total_seat = None
                if total_seat_text and total_seat_text.startswith("총"):
                    total_seat_num = re.sub(r'[^0-9]', '', total_seat_text)
                    if total_seat_num:
                        total_seat = total_seat_num
            else:
                hall_format = None
                hall_name = None
                total_seat = None

            time_table = hall.select_one("div.info-timetable ul")
            if not time_table:
                continue

            a_tags = time_table.select("li > a")
            for a_tag in a_tags:
                em_tag = a_tag.select_one("em")
                display_time = em_tag.get_text(strip=True) if em_tag else None

                seat_remain = a_tag.get("data-seatremaincnt")
                start_time_raw = a_tag.get("data-playstarttime")

                doc = {
                    "movie_title": movie_title,
                    "hall_name": hall_name,
                    "total_seat": total_seat,
                    "start_time": display_time,
                    "start_time_raw": start_time_raw,
                    "remain_seat": seat_remain,
                }
                results.append(doc)

    return results

if __name__ == "__main__":
    data = crawl_cgv_schedule()
    for idx, item in enumerate(data, start=1):
        print(f"[{idx}] 영화제목: {item['movie_title']}")
        print(f"     상영관: {item['hall_name']}")
        print(f"     총좌석: {item['total_seat']}")
        print(f"     상영시작(표시): {item['start_time']}")
        print(f"     상영시작(raw): {item['start_time_raw']}")
        print(f"     잔여좌석: {item['remain_seat']}")
        print("-----")

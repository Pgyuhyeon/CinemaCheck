import re
import json
import time  # 요청 간 딜레이 추가를 위한 모듈
from pymongo import MongoClient

# MongoDB 연결 설정
client = MongoClient("mongodb://localhost:27017/")  # 로컬 MongoDB의 기본 URL
db = client["theaterDB"]  # 데이터베이스 이름
collection = db["theaters"]  # 컬렉션 이름

# HTML 파일 읽기
with open("cgv.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# theaterJsonData 추출 (JavaScript 객체)
theater_data_match = re.search(r"var theaterJsonData = (\[.*?\]);", html_content, re.DOTALL)
if theater_data_match:
    theater_data = json.loads(theater_data_match.group(1))
    theaters = []
    for region in theater_data:
        region_code = region["RegionCode"]
        for theater in region["AreaTheaterDetailList"]:
            theater_name = theater["TheaterName"]
            theater_code = theater["TheaterCode"]
            theater_url = f"http://www.cgv.co.kr/theaters/?theaterCode={theater_code}"
            theater_doc = {
                "region_code": region_code,
                "theater_name": theater_name,
                "theater_code": theater_code,
                "theater_url": theater_url
            }
            theaters.append(theater_doc)
            
            # 요청 간 지연 시간 추가 (1~2초)
            time.sleep(1.5)  # 1.5초 지연

    # MongoDB에 데이터 삽입
    if theaters:
        collection.delete_many({})  # 기존 데이터 삭제
        collection.insert_many(theaters)
        print(f"{len(theaters)}개의 영화관 데이터가 MongoDB에 삽입되었습니다.")
else:
    print("theaterJsonData를 찾을 수 없습니다.")

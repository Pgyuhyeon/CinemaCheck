import re
from bs4 import BeautifulSoup
from pymongo import MongoClient

# MongoDB 연결 설정
client = MongoClient("mongodb://localhost:27017/")  # 로컬 MongoDB의 기본 URL
db = client["theaterDB"]  # 데이터베이스 이름
collection = db["theaters"]  # 컬렉션 이름

# HTML 파일 읽기
with open("megabox.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(html_content, "html.parser")

# 영화관 정보를 저장할 리스트
theaters = []

# 브랜드 이름 (메가박스)
brand_name = "메가박스"

# 영화관 리스트 추출
theater_list = soup.find_all("li", {"data-brch-no": True})
for theater in theater_list:
    theater_name = theater.find("a").text.strip()
    full_name = f"{brand_name}{theater_name}"  # 브랜드 이름 추가 및 띄어쓰기 제거
    branch_no = theater["data-brch-no"]
    
    # MongoDB에 저장할 문서
    theater_doc = {"name": full_name, "branch_no": branch_no}
    theaters.append(theater_doc)

# MongoDB에 데이터 삽입 (중복 방지)
if theaters:
    for theater in theaters:
        collection.update_one(
            {"branch_no": theater["branch_no"]},  # 중복 확인 조건
            {"$setOnInsert": theater},  # 중복이 없을 경우만 삽입
            upsert=True
        )
    print(f"{len(theaters)}개의 영화관 데이터가 MongoDB에 저장 또는 업데이트되었습니다.")
else:
    print("영화관 데이터를 찾을 수 없습니다.")

import requests
import json
import re
from pymongo import MongoClient

# URL 및 요청 데이터 설정
url = "https://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx"
param_list = json.dumps({
    "MethodName": "GetTicketingPageTOBE",
    "channelType": "HO",
    "osType": "W",
    "osVersion": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "memberOnNo": "0"
})

# Form-data 설정
files = {
    "paramList": (None, param_list)
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.lottecinema.co.kr",
    "Referer": "https://www.lottecinema.co.kr/NLCHS/Ticketing/Schedule"
}

# MongoDB 연결 설정
client = MongoClient("mongodb://localhost:27017/")  # 로컬 MongoDB의 기본 URL
db = client["theaterDB"]  # 데이터베이스 이름
collection = db["theaters"]  # 컬렉션 이름

# API 요청 보내기
response = requests.post(url, files=files, headers=headers)

# 응답 처리
if response.status_code == 200:
    try:
        data = response.json()  # JSON 데이터 파싱
        cinema_items = data.get("Cinemas", {}).get("Cinemas", {}).get("Items", [])
        
        # 영화관 이름과 코드를 매핑하여 MongoDB에 저장
        theaters = []
        for item in cinema_items:
            raw_name = item["CinemaNameKR"]
            # "롯데시네마"를 이름 앞에 붙이고 괄호와 괄호 안 내용을 제거
            cleaned_name = re.sub(r"\s*\(.*?\)", "", raw_name)
            theater_doc = {
                "name": f"롯데시네마 {cleaned_name}",
                "code": f"{item['DivisionCode']}|{item['DetailDivisionCode']}|{item['CinemaID']}"
            }
            theaters.append(theater_doc)
        
        # MongoDB에 데이터 삽입
        if theaters:
            collection.insert_many(theaters)
            print(f"{len(theaters)}개의 영화관 데이터가 MongoDB에 삽입되었습니다.")
        else:
            print("영화관 데이터가 없습니다.")
    except Exception as e:
        print("응답 데이터 처리 중 오류:", e)
else:
    print(f"요청 실패: {response.status_code}")

import requests
import time
import csv

# 카카오맵 API 키 설정
API_KEY = "c81b20db6a96b199e2fe6b8f1ea1cbed"
URL = "https://dapi.kakao.com/v2/local/search/category.json"

def fetch_theaters(x, y, radius=10000, max_pages=45):
    """특정 좌표(x, y)를 중심으로 반경 내 영화관 데이터를 가져옵니다."""
    headers = {
        "Authorization": f"KakaoAK {API_KEY}"
    }
    params = {
        "category_group_code": "CT1",  # 영화관
        "x": x,                       # 중심점 경도
        "y": y,                       # 중심점 위도
        "radius": radius,             # 반경 (최대 20,000m)
        "size": 15,                   # 한 페이지에 가져올 결과 수
        "page": 1                     # 페이지 번호
    }
    
    theaters = []
    while params["page"] <= max_pages:
        response = requests.get(URL, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            break
        
        data = response.json()
        theaters.extend(data["documents"])
        
        # 더 이상 데이터가 없으면 중단
        if len(data["documents"]) < params["size"]:
            break
        
        # 다음 페이지 요청
        params["page"] += 1
        time.sleep(0.5)  # 요청 제한 방지를 위해 딜레이 추가
    
    return theaters

# 서울 각 구의 중심 좌표
regions = [
    {"name": "종로구", "x": 126.9788, "y": 37.5730},
    {"name": "중구", "x": 126.9945, "y": 37.5640},
    {"name": "용산구", "x": 126.9723, "y": 37.5311},
    # 다른 구도 추가하세요
]

# 실행
all_theaters = []
for region in regions:
    print(f"Fetching theaters in {region['name']}...")
    theaters = fetch_theaters(region["x"], region["y"], radius=10000)
    all_theaters.extend(theaters)

# **CGV, 롯데시네마, 메가박스** 포함 필터링
filtered_theaters = [
    t for t in all_theaters
    if any(brand in t["place_name"] for brand in ["CGV", "롯데시네마", "메가박스"])
]

# 중복 제거
unique_theaters = {f"{t['place_name']}_{t['x']}_{t['y']}": t for t in filtered_theaters}

# CSV로 저장
with open("filtered_seoul_theaters.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["place_name", "road_address_name", "x", "y"])
    writer.writeheader()
    for key, theater in unique_theaters.items():
        writer.writerow({
            "place_name": theater["place_name"],
            "road_address_name": theater["road_address_name"],
            "x": theater["x"],
            "y": theater["y"]
        })

print(f"총 영화관 개수: {len(unique_theaters)}")

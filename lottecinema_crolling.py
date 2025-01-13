import json
import requests

url = "https://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx"

# 요청에 필요한 데이터를 form-data 형식으로 정의
param_list = json.dumps({
    "MethodName": "GetPlaySequence",
    "channelType": "HO",
    "osType": "W",
    "osVersion": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "playDate": "2025-01-13",
    "cinemaID": "1|0004|9070",
    "representationMovieCode": ""
})

# Form-data를 multipart로 전송하기 위한 설정
files = {
    "paramList": (None, param_list)  # key는 'paramList', value는 문자열화된 JSON
}

# 요청 헤더
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.lottecinema.co.kr",
    "Referer": "https://www.lottecinema.co.kr/NLCHS/Ticketing/Schedule"
}

# POST 요청 전송
response = requests.post(url, files=files, headers=headers)

# 응답 출력
print(response.status_code)
print(response.json())

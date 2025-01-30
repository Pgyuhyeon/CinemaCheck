### Team

---

## FE, 이현서

(고려대학교 컴퓨터학과 21학번)

[@ss-leg-al](https://github.com/ss-leg-al)

![IMG_4120 PNG](https://github.com/user-attachments/assets/382ced10-6c56-4cf1-88de-1bff3c7b9b19)


## BE, 박규현

(한양대학교 컴퓨터소프트웨어학부 22)

[@Pgyuhyeon](https://github.com/Pgyuhyeon/CinemaCheck)
![image](https://github.com/user-attachments/assets/a4c8a73d-b2bb-4551-941a-312b082443b0)



### Tech Stack

---

**프론트엔드** : React-Native, Typescript, expo

**백엔드** : Node.js, Express.js, MongoDB, mongoose, Postman, AWS, Python Crawling

**협업 툴** : Git, Github, Notion

### INTRO

---

# 01. CINEMACEHCK, 왜 만들었을까?

---
![image](https://github.com/user-attachments/assets/7005bf90-d0fb-4d38-aa85-57e6ab8423a0)



## *“영화관 다 찾아보기 귀찮다 ,,,”

       ”나는 큰 상영관이 좋은데,,”
                 
“나는 사람 많은데는 싫은데...”*

                

## “ 영화 상영시간표 한번에 못보나?”                   
                                                                                  ”영화관 정보 한번에 못보나,,,”
                                                                              ”너무 귀차나…ㅠㅠ”                                           **

## *”앱 3개를 다 돌아다녀야되네,,”*



# !!!!!!!!!!CINEMACHECK!!!!!!!!!!!

![image](https://github.com/user-attachments/assets/0cc5c7c2-222e-4dd2-ad16-2d5e94ba00d9)


### Details

---
![Simulator Screenshot - 13 - 2025-01-15 at 15 56 31](https://github.com/user-attachments/assets/95a2a466-b22d-4825-a3be-560074221bc4)

![Simulator Screenshot - 13 - 2025-01-15 at 15 56 50](https://github.com/user-attachments/assets/3231e561-3975-456d-8dae-948ebc8d7c43)


**시작 화면**

- 지도 위에 현재 위치 표기
- “현재 위치를 확인해주세요” 버튼 → 위치 권한 승인

![Simulator Screenshot - 13 - 2025-01-15 at 15 57 01](https://github.com/user-attachments/assets/7a8daecb-8f6d-4f06-8154-a32be91916cd)


**메인화면**

- 상영 중 섹션: 현재 상영작 카드 목록 (가로 스크롤)→ 클릭시 상영관 리스트 페이지로 이동
- 무대인사/이벤트 등 다양한 홍보 배너 (예: “CGV 할인 이벤트”)
- 영화관 3사 바로가기 배너(CGV,메가박스,롯데시네마)
![Simulator Screenshot - 13 - 2025-01-15 at 15 58 16](https://github.com/user-attachments/assets/205179db-4d9a-4049-85d6-d67d4f24fe68)

![Simulator Screenshot - 13 - 2025-01-15 at 16 06 44](https://github.com/user-attachments/assets/847bac18-67e3-4807-b70e-c2d6b7ca4565)


**영화별 상영시간표**

- 영화 클릭시 현재 위치정보 카카오 api요청 → 근처 영화문화시설 정보
- CGV, 메가박스, 롯데시네마 추출, 거리계산(경도, 위도)
- 저장된 데이터베이스(mongoDB, 10분 간격 업데이트) → 상영시간, 상영관, 잔여좌석 등의 정보 제공
- 잔여좌석은 10분간격으로 최신화 → 실시간 크롤링 활용(api 제공X)
- 상영시간표 해당 시간 클릭 → 해당 영화사 예매사이트로 이동
- 데이터베이스의 3일치 정보 저장 → 날짜 변경시 해당 정보 제공
![Simulator Screenshot - 13 - 2025-01-15 at 16 02 51](https://github.com/user-attachments/assets/7ea24b50-c53a-4d0b-9b8c-f178c6414411)

![Simulator Screenshot - 13 - 2025-01-15 at 16 03 08](https://github.com/user-attachments/assets/447270c0-0fd9-4dda-b563-2999a256f8c0)
![Simulator Screenshot - 13 - 2025-01-15 at 16 03 18](https://github.com/user-attachments/assets/eb8c80bf-bdc3-4ccf-b3b9-5a040213bb85)

**포토카드 만들기**

- 사용자 이름, 관람 일자, 관람 영화, 브랜드 선택
- 카드 레이아웃에 포스터 + 브랜드 로고 + 관람일자 + 이름을 넣어 포토카드 생성 후 **이미지**로 저장/공유
![Simulator Screenshot - 13 - 2025-01-15 at 16 04 59](https://github.com/user-attachments/assets/c3a0ff92-51f0-4041-81e7-01b4dfeea32d)

![Simulator Screenshot - 13 - 2025-01-15 at 16 06 09](https://github.com/user-attachments/assets/e953755b-3a35-4953-897b-45dfa91e5f96)


**상영 영화 미니게임**

- 현재 상영 중인 영화 중 랜덤으로 8개를 가져와 같은 포스터 찾기 미니게임 구현
- 카드를 뒤집어가며 같은 포스터를 찾고 완료한 시간에 따라 점수가 부여됨
- 시간이 초과되거나 게임이 종료되면 랜덤으로 상영 중인 영화를 추천

![Simulator Screenshot - 13 - 2025-01-15 at 16 16 44](https://github.com/user-attachments/assets/8fe01fbc-2834-46dd-b241-85fd388078a2)


**영화 전문가 챗봇**

- OpenAI를 이용한 영화 전문가 챗봇

## database

---



https://github.com/user-attachments/assets/8669f6d9-ad76-432b-8d83-32d99ca20c66


<img width="1425" alt="스크린샷 2025-01-15 오후 6 04 20" src="https://github.com/user-attachments/assets/6bc931ab-9bca-4208-a219-2d067f2c0a35" />



## 느낀점

---

### 박규현

- 백엔드를 처음 해봤는데 나쁘지 않았다
- 크롤링을 처음해봤는데 재밌었다
- 시간이 더있으면 최적화를 더 할수 있을것 같았다
- 옆에서 프론트가 뚝딱뚝딱 잘만들어서 편했다

### 이현서

- 배포하면 쓸만할 것 같은 앱을 만들었다
- 리액트네이티브>>>>>안드로이드스튜디오코틀린

# 교회 예배 ppt 자동 생성 프로그램 (bible2ppt)
*매주 예배 자료를 직접 만들다가 자동화하게 되었습니다.*

## 사용 방법
1. worship_info.csv에 정보를 적습니다.
<img width="308" alt="스크린샷 2020-11-17 오후 2 36 08" src="https://user-images.githubusercontent.com/49056225/99350703-5fce2f00-28e2-11eb-8c9a-8d307968ad78.png">

* rr : 성시교독 번호
* prayer : 대표 기도 담당자
* offering : 봉헌 찬양 담당자
* bible : 오늘의 말씀 (챕터, 시작 장, 시작 절, 끝 장, 끝 절)
* reader : 말씀 봉독 담당자
* sermon : 설교제목, 담당 목사


2. 아래와 같은 방법으로 실행합니다.
```
pipenv shell
pipenv install
python bible2ppt.py
```

3. 'yyyy-mm-dd.pptx'라는 ppt 파일이 생성됩니다.
* 예시 화면
<img width="690" alt="스크린샷 2020-11-17 오후 2 57 33" src="https://user-images.githubusercontent.com/49056225/99352062-4c709300-28e5-11eb-97e6-b0b5bcf12a7c.png">
<img width="693" alt="스크린샷 2020-11-17 오후 2 57 41" src="https://user-images.githubusercontent.com/49056225/99352098-5c887280-28e5-11eb-990e-9cfd394102ca.png">


## 사용 기술
* 언어 : python
* Web crawling : 웹 사이트에서 '성시교독'을 크롤링 한 후 'responsive_reading.csv'에 저장
* Web API : 성경 구절을 가지고 오기 위해 사용 (http://m.ibibles.net/quote10.htm)
* 라이브러리 : beautifulSoup4, requests, python-pptx

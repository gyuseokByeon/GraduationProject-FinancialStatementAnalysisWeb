# For The Ants

![issue_badge](https://img.shields.io/badge/python-3.8-blue?style=flat)
![issue_badge](https://img.shields.io/badge/django-3.7.1-blue?style=flat)
![issue_badge](https://img.shields.io/badge/tailwindcss-6.14.11-blue?style=flat)
![issue_badge](https://img.shields.io/badge/pandas-1.2.3-blue?style=flat)
![issue_badge](https://img.shields.io/badge/numpy-1.20.1-blue?style=flat)
![YouTube Video Views](https://img.shields.io/youtube/views/PR4RI2n3VL8?style=social)
### 개인 투자자를 위한 재무제표 분석 및 시각화 웹 앱
##### 개발 기간 : 20.08 ~ 21.06, 21.12 ~ 리팩토링
### Financial statements analysis and visualization web apps for individual investors


</br>

* #### :family: 개발자
  * 권우석

* #### :computer:
  * Language & Environment: HTML5, CSS, Python, Javascript
  * Frameworks: TailwindCss, Django
  * Library: pandas, numpy, jquery, etc...

* #### :file_folder: Server
  * AWS Elastic Beanstalk: 웹 서버
  * AWS RDS: DB 서버

* #### :iphone: Crawler
  * Periodic Crawler for stock price data: 네이버 금융 / 매일 오후 5시 / 시가, 종가, 저가, 고가, 거래량 
  * Crawler: 금융감독원 Open API / 연 4회 / 재무상태표, 손익계산서 주요 항목

<hr/>

</br>

## 1. 프로젝트 배경

  
![picture 1](https://user-images.githubusercontent.com/62459196/146550617-d89d44b3-dcd6-4996-9d38-c3e295e4e75d.png)
  
 - 졸업작품 중간 발표: [프로젝트 설명 영상(Click)](https://youtu.be/PR4RI2n3VL8?t=0s)  
 - 졸업작품 개발 후기: [문돌이의 SW학부 졸업작품 도전기 (Click)](https://blog.naver.com/rnjsdntjr26/222387156770)   
 

 
## 2. 프로젝트 구성도

  
![project1](https://github.com/egg528/egg528.github.io/blob/master/imgs/project1.png?raw=true)  


 ## 3. 주요 기능
####    
  
![](https://github.com/egg528/egg528.github.io/blob/master/gifs/project1.gif?raw=true)  

#### (1) 5개년 분기별 재무 데이터 엑셀 다운로드
- Periodic Crawler와 금융감독원 OPENAPI를 바탕으로 수집한 주가/재무 데이터 5개년치를 클릭 한번으로 다운받을 수 있는 기능
- 해당 기능을 통해 재무 분석을 위한 무의미한 반복 노동(재무제표 복.붙)을 없애, 개인투자자들은 간편하게 자신만의 기업 분석이 가능합니다.        


#### (2) 주요 재무 항목 시각화
![picture 4](https://user-images.githubusercontent.com/62459196/146550682-c77be4e0-b87e-4668-ac70-436f43318053.png)  

#### (3) 주가와 상관관계가 가장 높은 재무 항목 제시 (기업별)

  ![picture 5](https://user-images.githubusercontent.com/62459196/146550686-5ccbed5f-61d7-4bd6-b804-b3f122c1e925.png)

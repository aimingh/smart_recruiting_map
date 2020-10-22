# smart_recruiting_map  
### 팀명 - 위오동맹


<br>
본 프로젝트는 한국전파진흥협회 에서 진행되는 '5G 영상처리를 활용한 AI 자율비행 통제시스템' 에서 진행되었습니다.

총 2가지를 주제로 제작되었으며 주제는 아래와 같습니다.
<br><br>

    공통 주제 - 100대 명산 맵과 정보 리스트

    팀 주제 - 구직정보 데이터를 기반한 맵

<br><br>
프로젝트의 개발환경은 아래와 같습니다.

    OS : ubuntu 20.04
    언어 : Python, html
    프레임워크 : Django, BootStrap
    데이터베이스 : MongoDB(Docker)
    편집기 및 디버거 - Visual studio code
    파이썬 라이브러리 - Django,selenium,folium,bs4,
                       requsts,pymongo,pandas,urllib


<br>


# Index 

1. 스토리 보드

2. 페이지 구도

3. 페이지 상세설명
<br>
<br>
<br>



## 1.스토리 보드

본 페이지는 django 를 통해 제작되었으며, 2개의 주제에 해당하는 App을 구성 하였습니다.
크게 아래의 구도로 이어집니다.

<br>

    Homepage/ ㅡ mountain/ ㅡ mountain_map/ ㅡ info/
              ㄴ  Job/     ㅡ job_map_search/
                           ㄴ job_map_all/


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


<br>
<br>
이미지로는 다음과 같습니다

<img src='pictures/스토리보드.png'>

메인 페이지로부터 왼쪽은 100대 명산을 위한 App 이며 오른쪽은 구직정보를 기반으로 한 map 을 위한 APP 입니다.

공통으로는 Navivar 를 통해 mainpage, /moutain/moutain_mapp, /Job/job_map_search, /Job/job_mal_all 

까지 접속이 가능합니다.

<br>
<br>
<br>
<br>

# 2. 페이지 구도

<br>
<br>

### 1. 메인 페이지

<img src='pictures/스크린샷, 2020-10-22 14-12-04.png'>

<br>
<br>

    메인 페이지에서는 구성된 2개의 앱에 대한 간단한 설명과 팀원이 한 작업에 대해 설명하고있습니다.
    Navar 를 통해서도 2개의 앱에 각각 접속이 가능하며, 아래 page discription 을 통해 접속이 가능합니다.


<br>
<br>

### 2. Mountain map

<br>

Moutain Map 은 Blackyak과 산림청에서 지정한 100대 명산에 대한 정보를 정리하고, 이를 모아놓은 맵을 나타낸 페이지입니다.

가장 처음 페이지에 접속하면 아래와 같이 100개의 명산위치를 아이콘으로 표시한 맵이 나옵니다.

<br><br>

사진을 클릭하면 영상이 나옵니다.

[![view moutain](https://github.com/blackcoke/smart_recruiting_map/blob/master/pictures/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%2C%202020-10-22%2014-12-15.png)](https://www.youtube.com/watch?v=WThlCfFKSes) 



<br>
<br>

맵 하단에는 산에 대한 정보를 간략이 정리해 둔 리스트가 나와있습니다. 
리스트를 클릭하면 아래와 같은 페이지가 나오며, 산에 대한 대략적인 설명과 GPS 좌표 및 주소를 표시하였고, 맵에 해당하는 위치가 Zoom 이 됩니다.

<br>
<br>

사진을 클릭하면 영상이 나옵니다.

[![view moutain](https://github.com/blackcoke/smart_recruiting_map/blob/master/pictures/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%2C%202020-10-22%2014-12-20.png)](https://www.youtube.com/watch?v=EocjhoD8394)

위 영상과 같이 상세페이지에서 다시 목록페이지로 이동이 가능합니다.

<br>
<br>
<br>
<br>

### 3. Job recruit 페이지 

<br>
<br>
본 페이지는 jobkorea로 부터 구인 정보를 얻어 온 후, 회사의 위치를 통해 맵에 보여줍니다.
아래 사진은 처음 페이지를 이동했을 때의 모습을 보여주며 사진을 클릭시 어떻게 검색하고 들어가는지 알 수 있는 영상으로 보내줍니다.

<br>
사진을 클릭하면 영상이 나옵니다.

[![job korea](https://github.com/blackcoke/smart_recruiting_map/blob/master/pictures/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%2C%202020-10-22%2014-12-23.png)](https://www.youtube.com/watch?v=lbxM-8EEdiA)

<br>

    영상과 같이 경력 / 키워드 / 페이지 수를 결정 후 submit 버튼을 눌러 검색을 합니다.
    검색이 완료되면 구인정보가 등록된 회사의 위치를 맵으로 표기해주며 list 버튼을 누르면 이를 리스트로 정리한 페이지로 이동이 가능합니다.
    맵의 하단에 해당 구직 정보에 대한 리스트를 보여주고, 리스트를 클릭하면 해당 페이지로 이동이 가능합니다.
    리스트 사진은 아래와 같습니다.

<img src='https://github.com/blackcoke/smart_recruiting_map/blob/master/pictures/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%2C%202020-10-22%2014-13-30.png'>


또한 검색한 데이터가 나와 있는 맵의 형태를 Clusting Map 과 Heat Map 이 두 버튼을 통해 바꿀 수 있습니다. 


a. Cluster map

아래에는 Cluster 형 맵을 나타냈습니다.
정보가 많다면 아이콘이 많이 겹칠 수 가 있는데, 이를 방지하기 위한 아이콘 표기형 맵입니다.
일정 구역내에 아이콘이 겹친다면 겹치는 숫자를 표기하여 아이콘에 나타내줍니다.

사진을 클릭하면 영상이 나옵니다.

[![job korea](https://github.com/blackcoke/smart_recruiting_map/blob/master/pictures/cluster.png)](https://www.youtube.com/watch?v=CZDYkJnZGT8)

b. Heat Map 

아래사진은 구직정보를 담은 맵을 hitmap 으로 나타낸 사진입니다.
구직정보가 주로 몰린곳을 시각적으로 확인이 가능합니다.
이 또한 확대를 통해 몰린 지역을 상세하게 볼 수 있습니다.

<img src='https://github.com/blackcoke/smart_recruiting_map/blob/master/pictures/hitmap_job.png'>


### 3. Worknet 구인구직 hitmap 

이 페이지는 worknet 에 등록된 대기업,중소기업,강소기업,공기업의 구인정보를 담은 데이터 베이스로부터 
위치정보를 얻어와서 현재 어느지역이 구인정보가 몰려있는지 확인 가능한 페이지입니다.
현재 데이터가 대략 5500개 정도 존재합니다.

이 역시 아래 사진과 같이 확대해서 확인이 가능합니다.

[![job korea](https://github.com/blackcoke/smart_recruiting_map/blob/master/pictures/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%2C%202020-10-22%2014-13-10.png)](https://www.youtube.com/watch?v=hpPhuBngHyk)





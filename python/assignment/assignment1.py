#1

"""
영화 목록 API를 이용하여 감독의 이름이 "봉준호"인 영화의 목록을 받아 데이터 프레임을 생성한 후, 
'prdtYear'변수를 기준으로 오름차순을 정렬하세요. 
'directors'컬럼과 'companys'컬럼은 이름만 남도록 변경해주세요.
"""


import requests
import pandas as pd
from bs4 import BeautifulSoup
import bs4
import json

key="954ce697f4d9258d1d0e1e38925b1dd3"
directorNm = "봉준호"
url=f"http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={key}&directorNm={directorNm}"
result = requests.get(url)
html = result.json()

# 판다스 사용.. 
DF = pd.DataFrame(html['movieListResult']["movieList"])

# 연도로 다시 정렬
DF = DF.sort_values("prdtYear")

# 컬럼 형식 바꾸기
DF['directors'] = DF['directors'].apply(lambda x : x[0]['peopleNm'])
DF['companys'] = DF['companys'].apply(lambda x : x[0]['companyNm'] if x else x)

print(DF)


#1-2

"""
일별 박스오피스 API를 이용하여 
2018년의 한국 영화 일별 박스오피스 데이터를 생성하여 csv파일로 저장하세요.
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import bs4
import json

## 날짜를 먼저 만들어준다. -> 시간 데이터 만들기
date = pd.date_range('20180101', '20181231')
Time = []
for time in date:
    Time.append(date.strftime("%Y%m%d").tolist())

time_list=Time[0] ##12번 반복됨을 알아서 그중에서 하나만 사용

data = []
key = "954ce697f4d9258d1d0e1e38925b1dd3"
url = "http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key=" + key + "&targetDt="

df_default = pd.DataFrame()
for k in range(len(time_list)):
    requestData2 = requests.get(url + str(time_list[k]) + '')
    data_2 = requestData2.json()
    data = data_2['boxOfficeResult']['dailyBoxOfficeList']
    df = pd.DataFrame.from_dict(data)
    df_default = df_default.append(df)

## 한글이 포함되어 있으므로, encoding에 utf-8을 넣는다.-> 파일을 저장한다.
df_default.to_csv('data_result.csv',encoding='utf-8', index = False)

## 출력을 통해서 확인
pd.read_csv('data_result.csv')


# 2의 예시문제

# 예시 문제

"""
멜론의 Top100 차트 데이터를 크롤링해 
곡 명, 가수 명, 앨범 명 데이터를 만들어 봅시다.
"""

"""
Selenium을 통해 웹을 동작시킨 후, 
전과 같이 BeautifulSoup을 통해 html 정보를 parsing하고 원하는 데이터를 가져올 것
"""

import selenium
from selenium import webdriver as wd
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
from itertools import repeat

driver = wd.Chrome('.\chromedriver') # 크롬드라이버 경로
driver.maximize_window() # 크롬창 크기 최대

# 드라이버가 해당 url 접속
url = 'https://www.melon.com/chart/index.htm' # 멜론차트 페이지
driver.get(url)

html = driver.page_source # 드라이버 현재 페이지의 html 정보 가져오기

soup = BeautifulSoup(html, 'html.parser')
# class 찾아서 가져오기
title = soup.find_all('div', class_ = 'ellipsis rank01')
singer = soup.find_all('span', class_ = 'checkEllipsis')
album = soup.find_all('div', class_ = 'ellipsis rank03')

title_list = []
singer_list = []
album_list = []

length  = len(title) #100
for i in range(0, length, 1): # append를 통해서 각 리스트에 넣어준다.
    title_list.append(title[i].text.strip("\n"))
    singer_list.append(singer[i].text)
    album_list.append(album[i].text.strip("\n"))
    
# 데이터 프레임에 넣어준다.
df_1= pd.DataFrame()
df_1['title'] = title_list
df_1['singer'] = singer_list
df_1['album'] = album_list

driver.close()
df_1


#2 

"""
월간 차트 페이지에서 2021년 1월부터 12월까지의 월간 차트를 모아 하나의 데이터 프레임을 만드세요. 
칼럼은 총 8개로 연, 월, 순위, 순위 변동, 곡 명, 가수 명, 앨범 명, 좋아요 수입니다.
"https://arehoow.tistory.com/10 사이트를 참고해서 코드 작성해주시면 됩니다
"""

def melon(mon):
    global df_reset
    # 크롬드라이버 열기
    driver = wd.Chrome('.\chromedriver') # 크롬드라이버 경로
    driver.maximize_window() # 크롬창 크기 최대
        
    # 드라이버가 해당 url 접속
    url = 'https://www.melon.com/chart/index.htm' # 멜론차트 페이지
    driver.get(url)
    
    # 차트파인더 클릭
    driver.find_element_by_xpath('//*[@id="gnb_menu"]/ul[1]/li[1]/div/div/button/span').click()
    
    # 연대선택, 연도선택, 월선택, 장르선택
    
    # 월간차트 클릭
    driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/h4[2]/a').click()
    time.sleep(2)
    
    # 연대선택 2020년대 클릭
    driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[1]/div[1]/ul/li[1]/span/label').click()
    time.sleep(2)
    
    # 연도선택 2021년 클릭
    driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[2]/div[1]/ul/li[2]/span/label').click()
    time.sleep(2)
    
    # 월선택 month월 클릭
    driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[3]/div[1]/ul/li['+str(mon)+']/span/label').click()
    time.sleep(2)
    
    # 장르선택 종합 클릭
    driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[5]/div[1]/ul/li[1]/span/label').click()
    time.sleep(2)
   
    # 검색버튼 클릭
    driver.find_element_by_xpath('//*[@id="d_srch_form"]/div[2]/button/span/span').click()
    time.sleep(2)
    
    html = driver.page_source # 드라이버 현재 페이지의 html 정보 가져오기
    soup = BeautifulSoup(html, 'html.parser')
    
    #  연, 월, 순위, 순위 변동, 곡 명, 가수 명, 앨범 명, 좋아요 수
    title = soup.find_all('div', class_ = 'ellipsis rank01')
    singer = soup.find_all('span', class_ = 'checkEllipsis')
    album = soup.find_all('div', class_ = 'ellipsis rank03')
    diff = soup.find_all('span', class_ = 'wrap_rank')
    like = soup.find_all('span', class_ = 'cnt')
    

    
    ## 리스트 초기화
    year_list = []
    month_list = []
    rank_list = []
    diff_list = []
    title_list = []
    singer_list = []
    album_list = []
    like_list = []
    
    ength  = len(title) # 100
    
    for i in range(0, length, 1):
    ## 만들어준 리스트에 append를 통해서 담아준다.
        year_list.append(2021)
        month_list.append(mon)
        rank_list.append(i+1)
        title_list.append(title[i].text.strip("\n").replace("\n", " ")) ## 결과를 보니까 중간에 들어간 \n 존재해서 이를 띄어쓰기로 대체
        singer_list.append(singer[i].text)  
        like_list.append(like[i].text.strip("\n")[4:])
        album_list.append(album[i].text.strip("\n"))
        diff_list.append(diff[i+10]['title'])
        
    ## 빈 데이터 프레임을 만들어서 담아준다 -> 함수를 돌릴 때, 각 함수에서 나온 결과를 담아놓는 dataframe이 필요
    ## 이를 계속 append 해서 최종 dataframe을 만든다.
    df= pd.DataFrame()
    df["year"] = year_list
    df["month"] = month_list
    df['rank'] = rank_list
    df['diff'] = diff_list
    df['title'] = title_list
    df['singer'] = singer_list
    df['album'] = album_list
    df['like'] = like_list
    
    df_reset = df_reset.append(df) #dataframe 결과를 쌓아주는 역할을 한다.
    driver.close() #드라이버가 여러개 열리면 복잡하므로 사용후 닫아준다.
    
df_reset = pd.DataFrame()## 빈 데이터 프레임 만들기
for i in range(1, 13, 1): ## 반복문으로 12개월을 한번에 돌리면 끝
    melon(i)
df_reset = df_reset.reset_index(drop=True)   
df_reset

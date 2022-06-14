# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 23:28:22 2022

@author: dali1
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time


chromedriver = '/C:/Users/dali1' 
driver = webdriver.Chrome(chromedriver) 

# 포스팅 작성 당시 크롬 버젼 : 92


# 네이버 지도 검색창에 [~동 @@식당]으로 검색해 정확도를 높여야 합니다. 검색어를 미리 설정해줍시다.

df['naver_keyword'] = df['dong'] + "%20" + df['name']  # "%20"는 띄어쓰기를 의미합니다.
df['naver_map_url'] = ''


# 본격적으로 가게 상세페이지의 URL을 가져옵시다

for i, keyword in enumerate(df['naver_keyword'].tolist()):
    print("이번에 찾을 키워드 :", i, f"/ {df.shape[0] -1} 행", keyword)
    try:
        naver_map_search_url = f"https://m.map.naver.com/search2/search.naver?query={keyword}&sm=hty&style=v5"
        
        driver.get(naver_map_search_url)
        time.sleep(3.5)
        df.iloc[i,-1] = driver.find_element_by_css_selector("#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview").get_attribute('data-cid')
        # 네이버 지도 시스템은 data-cid에 url 파라미터를 저장해두고 있었습니다.
        # data-cid 번호를 뽑아두었다가 기본 url 템플릿에 넣어 최종적인 url을 완성하면 됩니다.
        
        #만약 검색 결과가 없다면?
    except Exception as e1:
        if "li:nth-child(1)" in str(e1):  # -> "child(1)이 없던데요?"
            try:
                df.iloc[i,-1] = driver.find_element_by_css_selector("#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview").get_attribute('data-cid')
                time.sleep(1)
            except Exception as e2:
                print(e2)
                df.iloc[i,-1] = np.nan
                time.sleep(1)
        else:
            pass


driver.quit()


# 이때 수집한 것은 완전한 URL이 아니라 URL에 들어갈 ID (data-cid 라는 코드명으로 저장된) 이므로, 온전한 URL로 만들어줍니다

df['naver_map_url'] = "https://m.place.naver.com/restaurant/" + df['naver_map_url']


# URL이 수집되지 않은 데이터는 제거합니다.
df = df.loc[~df['naver_map_url'].isnull()]

# 크롤링 에러가 떠서 'null'을 넣어 둔 데이터는 활용 의미가 없으므로 행 삭제를 해줘도 됩니다
df = df.loc[~(df['naver_store_type'].str.contains('null'))]


# 별점 평균, 수 같은 데이터 역시 스트링 타입으로 크롤링이 되었으므로 numeric으로 바꿔줍니다.
df[['naver_star_point', 'naver_star_point_qty', 'naver_blog_review_qty']] = df[['naver_star_point', 'naver_star_point_qty', 'naver_blog_review_qty']].apply(pd.to_numeric)
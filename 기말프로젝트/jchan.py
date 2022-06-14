import pandas as pd
import json
import requests
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time

decode_serviceKey = 'g9uyVk1xMZNy1G+bBKcWE6O0ywsy+3Om+NA/2B+KUvULR+Dg9uiN+z5S+XFoFnGQOE22ooo5GHovHau0HpNW7w=='    
ednode_serviceKey = 'g9uyVk1xMZNy1G%2BbBKcWE6O0ywsy%2B3Om%2BNA%2F2B%2BKUvULR%2BDg9uiN%2Bz5S%2BXFoFnGQOE22ooo5GHovHau0HpNW7w%3D%3D'

#1159053000
def getDivId(signguCd,adongNm):
    #signguCd = '11590' 동작구     
    url = 'http://apis.data.go.kr/B553077/api/open/sdsc2/baroApi?resId=dong&catId=admi'+'&serviceKey=' + ednode_serviceKey + '&signguCd=' + signguCd + '&type=json'
        
    response_json = requests.get(url, allow_redirects=False)
    response = json.loads(response_json.content)
    responseArr = response.get('body').get('items')
            
    _return = ''
    for list in responseArr:
        if str(list.get('adongNm')) == adongNm :
            _return = list.get('adongCd')
                
        if(_return == ''):
            _return = 'Not found'
            
    return _return

def getCommercialArea(signguCd, adongNm):
        
    #params
    url = 'http://apis.data.go.kr/B553077/api/open/sdsc2/storeListInDong'
    divId = 'adongCd'
    key = str(getDivId(signguCd,adongNm))
    params ={'serviceKey' : decode_serviceKey, 'pageNo' : '1', 'numOfRows' : '1000', 'divId' : divId, 'key' : key, 'type' : 'json' }
        
    response_json = requests.get(url, params=params, allow_redirects=False)
    response = json.loads(response_json.content)
    responseArr = response.get('body').get('items')
        
    #테스트 필요
    page = response.get('body').get('totalCount') // 1000 + 1
    if page > 1 :
        for p in range(1, page):
            params['pageNo'] = str(p)
            add_response_json = requests.get(url, params=params, allow_redirects=False)
            add_response = json.loads(add_response_json.content)
            add_responseArr = add_response.get('body').get('items')
            responseArr = responseArr + add_responseArr
            
    _return = pd.DataFrame(responseArr)
    
    return _return

### 최대반경 2km
# def getStoreListInRadius(cx, cy):
#     storeList = []
#     for key, value in {'병원': 'S01', '백화점': 'D03B01', '영화관': 'N03A01'}.items():
#         #params
#         url = 'http://apis.data.go.kr/B553077/api/open/sdsc2/storeListInRadius'
#         params = {'serviceKey' : decode_serviceKey, 'pageNo' : '1', 'numOfRows' : '1000', 'radius' : '2000', 'cx' : cx, 'cy' : cy, 'type' : 'json' }
#         if key == '병원':
#             params['indsMclsCd'] = value
#         else:
#             params['indsSclsCd'] = value
        
#         response_json = requests.get(url, params=params, allow_redirects=False)
#         response = json.loads(response_json.content)
#         storeList.append(response.get('body').get('items'))
        
#     hospital = pd.DataFrame(storeList[0])
#     store = pd.DataFrame(storeList[1])
#     theater = pd.DataFrame(storeList[2])
#     return hospital, store, theater

#네이버 지도 방문자리뷰수, 블로그리뷰수 지도 시각화
#!pip install folium
import folium
import pandas as pd

def setMap():
    review_map = folium.Map(location=[37.4873, 126.9510], zoom_start=14)

    ssu_review = pd.read_csv('./숭실대-리뷰수2.csv', encoding='UTF-8', engine='python')
    su_review = pd.read_csv('./서울대-리뷰수.csv', encoding='UTF-8', engine='python')
    jau_review = pd.read_csv('./중앙대-리뷰수.csv', encoding='UTF-8', engine='python')

    def getReview(review):
        review_geoData = review[['bizesNm', 'lon', 'lat', 'naver_store_type', 'naver_blog_review_qty']]
        return review_geoData.sort_values('naver_blog_review_qty', ascending=False)    

    for i, store in getReview(ssu_review).head(10).iterrows(): 
        popup = '<div style="width:150px;height:80px"><div>숭실대학교</div><div>상호명 : %s</div><div>분류 : %s</div><div>블로그리뷰수 : %s</div></div>' % (store['bizesNm'],store['naver_store_type'],store['naver_blog_review_qty'])
        folium.Marker(location=[store['lat'],store['lon']], popup=popup, icon=folium.Icon(color='blue')).add_to(review_map)

    for i, store in getReview(su_review).head(10).iterrows(): 
        popup = '<div style="width:150px;height:80px"><div>서울대학교</div><div>상호명 : %s</div><div>분류 : %s</div><div>블로그리뷰수 : %s</div></div>' % (store['bizesNm'],store['naver_store_type'],store['naver_blog_review_qty'])
        folium.Marker(location=[store['lat'],store['lon']], popup=popup, icon=folium.Icon(color='yellow')).add_to(review_map)

    for i, store in getReview(jau_review).head(10).iterrows(): 
        popup = '<div style="width:150px;height:80px"><div>중앙대학교</div><div>상호명 : %s</div><div>분류 : %s</div><div>블로그리뷰수 : %s</div></div>' % (store['bizesNm'],store['naver_store_type'],store['naver_blog_review_qty'])
        folium.Marker(location=[store['lat'],store['lon']], popup=popup, icon=folium.Icon(color='orange')).add_to(review_map)

    review_map.save('./학교별리뷰수.html')
    
    reviewMean_dict = {}
    reviewMean_dict['ssu'] = getReview(ssu_review)['naver_blog_review_qty'].mean()
    reviewMean_dict['su'] = getReview(su_review)['naver_blog_review_qty'].mean()
    reviewMean_dict['jau'] = getReview(jau_review)['naver_blog_review_qty'].mean()
    _return = pd.DataFrame(reviewMean_dict, index=[0])
    _return.index = ['리뷰수 평균']
    
    return _return
    
### 필요한 인자가 시군구코드, 찾을행정동
class CommercialArea:
    def __init__(self, signguCd, adongNm, cx, cy):
        self._signguCd = signguCd
        self._adongNm = adongNm
        self._cx = cx #경도
        self._cy = cy #위도
        
    def getDf(self):
        _return = getCommercialArea(self._signguCd, self._adongNm)
        return _return
    
    def getCoordinate(self):
        _return = getStoreListInRadius(self._cx, self._cy)
        return _return
    
    
import pandas as pd
import json
import requests

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
def getStoreListInRadius(cx, cy):
    storeList = []
    for key, value in {'병원': 'S01', '백화점': 'D03B01', '영화관': 'N03A01'}.items():
        #params
        url = 'http://apis.data.go.kr/B553077/api/open/sdsc2/storeListInRadius'
        params = {'serviceKey' : decode_serviceKey, 'pageNo' : '1', 'numOfRows' : '1000', 'radius' : '2000', 'cx' : cx, 'cy' : cy, 'type' : 'json' }
        if key == '병원':
            params['indsMclsCd'] = value
        else:
            params['indsSclsCd'] = value
        
        response_json = requests.get(url, params=params, allow_redirects=False)
        response = json.loads(response_json.content)
        storeList.append(response.get('body').get('items'))
        
    hospital = pd.DataFrame(storeList[0])
    store = pd.DataFrame(storeList[1])
    theater = pd.DataFrame(storeList[2])
    return hospital, store, theater
    
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
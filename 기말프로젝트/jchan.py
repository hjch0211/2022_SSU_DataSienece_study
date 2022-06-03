import pandas as pd
import json
import webbrowser
import time
import requests

### 필요한 인자가 시군구코드, 찾을행정동
class CommercialArea: 
    decode_serviceKey = 'NwS7t35ZvejHIExKbCymXgmyoLk0WLkZKDslnArD0xyBdUm3ohgWtefXVg25j9L9z3UdyDXXWbfIVjwGfOFArw=='    
    ednode_serviceKey = 'NwS7t35ZvejHIExKbCymXgmyoLk0WLkZKDslnArD0xyBdUm3ohgWtefXVg25j9L9z3UdyDXXWbfIVjwGfOFArw%3D%3D'
        
    ### getCommercialArea(행정동코드)
    def getCommercialArea(self, signguCd, adongNm):
        ### getDivId(구코드, 찾을 행정동)
        def getDivId():
            #signguCd = '11590' 동작구
            webbrowser.open("http://apis.data.go.kr/B553077/api/open/sdsc2/baroApi")
            time.sleep(2) #임시 비동기 처리
            
            url = 'http://apis.data.go.kr/B553077/api/open/sdsc2/baroApi?resId=dong&catId=admi'+'&serviceKey=' + self.ednode_serviceKey + '&signguCd=' + signguCd + '&type=json'
            
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
        
        webbrowser.open("http://apis.data.go.kr/B553077/api/open/sdsc2/storeListInDong")
        time.sleep(2) #임시 비동기 처리
        
        #params
        url = 'http://apis.data.go.kr/B553077/api/open/sdsc2/storeListInDong'
        divId='adongCd'
        key = getDivId()
        params ={'serviceKey' : self.decode_serviceKey, 'pageNo' : '1', 'numOfRows' : '1000', 'divId' : divId, 'key' : key, 'type' : 'json' }
        
        response_json = requests.get(url, params=params, allow_redirects=False)
        response = json.loads(response_json.content)
        responseArr = response.get('body').get('items')

        _return = pd.DataFrame(responseArr)
        
        #테스트 필요
        page = response.get('body').get('totalCount') // 1000 + 1
        if page > 1 :
            for p in range(1, page):
                params['pageNo'] = str(p)
                add_response_json = requests.get(url, params=params, allow_redirects=False)
                add_response = json.loads(add_response_json.content)
                add_responseArr = add_response.get('body').get('items')
                responseArr = responseArr + add_responseArr
                
        return _return
        
##이런식으로 사용하면 됨
#test = CommercialArea()
#print(test.getCommercialArea('11590', '상도1동')
##리펙토링 마렵네요..
from jchan import CommercialArea

test = CommercialArea('11590', '상도1동')
test.getDf()

### df에서
# bizesNm : 건물명
# indsLclsNm : 상권업종대분류명
# indsSclsCd : 상권업종소분류명
# lon : 경도
# lat : 위도
# 주로 위 데이터사용하면 될거야
### 객체.getDf().loc[0,:] 로 확인해봐도 좋고

print(test.getDf().loc[0,:])
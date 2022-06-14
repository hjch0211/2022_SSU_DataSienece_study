from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import numpy as np




# 서브 드라이버 : 블로그 리뷰 텍스트를 리뷰 탭 들어가서 크롤링
# sub_driver = webdriver.Chrome('chromedriver')
def load_data(df):
    
    driver = webdriver.Chrome('chromedriver') 

    df['naver_keyword'] = df['bizesNm'] + '%20' + df['adongNm']  # "%20"는 띄어쓰기를 의미합니다.
    df['naver_map_url'] = ''


    for i, keyword in enumerate(df['naver_keyword'].tolist()):
        print("이번에 찾을 키워드 :", i, f"/ {df.shape[0] -1} 행", keyword)
        try:
            naver_map_search_url = f"https://m.map.naver.com/search2/search.naver?query={keyword}&sm=hty&style=v5"
            
            driver.get(naver_map_search_url)
            driver.implicitly_wait(1.5)
            df.iloc[i,-1] = driver.find_element(By.CSS_SELECTOR, "#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview").get_attribute('data-cid')
            print(df.iloc[i,-1])
            # 네이버 지도 시스템은 data-cid에 url 파라미터를 저장해두고 있었습니다.
            # data-cid 번호를 뽑아두었다가 기본 url 템플릿에 넣어 최종적인 url을 완성하면 됩니다.
            
            #만약 검색 결과가 없다면?
        except Exception as e1:
            if "li:nth-child(1)" in str(e1):
                try:
                    df.iloc[i,-1] = driver.find_element(By.CSS_SELECTOR, "#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview").get_attribute('data-cid')
                    driver.implicitly_wait(1)
                except Exception as e2:
                    print(e2)
                    df.iloc[i,-1] = np.nan
                    driver.implicitly_wait(1)
            else:
                pass


    driver.quit()


    # 이때 수집한 것은 완전한 URL이 아니라 URL에 들어갈 ID (data-cid 라는 코드명으로 저장된) 이므로, 온전한 URL로 만들어줍니다
    df['naver_map_url'] = "https://m.place.naver.com/restaurant/" + df['naver_map_url']


    # URL이 수집되지 않은 데이터는 제거합니다.
    df = df.loc[~df['naver_map_url'].isnull()]


    naver_map_name_list = []
    blog_review_list = []
    blog_review_qty_list = []
    naver_map_star_review_stars_list = []
    naver_map_star_review_qty_list = []
    naver_map_type_list = []
    from tqdm.notebook import tqdm
    # 메인 드라이버 : 별점 등을 크롤링
    driver = webdriver.Chrome('chromedriver') 
    
    
    
    for i, url in enumerate(tqdm(df['naver_map_url'])):
    
        driver.get(url)
      #   sub_driver.get(url+"/review/ugc")
        driver.implicitly_wait()
    
        try:
            
            # 네이버 지도의 유형 분류
            naver_map_type = driver.find_element(By.CSS_SELECTOR,"#_title > span._3ocDE").text
    
            # 블로그 리뷰 수
            blog_review_qty = driver.find_element(By.CSS_SELECTOR,"#app-root > div > div > div > div.place_section.GCwOh > div._3uUKd > div._20Ivz > span:nth-child(2) > a > em").text
            print(blog_review_qty)
    
            naver_map_type_list.append(naver_map_type)
            blog_review_qty_list.append(blog_review_qty)

    
        # 리뷰가 없는 업체는 크롤링에 오류가 뜨므로 표기해둡니다.
        except Exception as e1:
            print(f"{i}행 문제가 발생")
            
            # 리뷰가 없으므로 null을 임시로 넣어줍니다.
            blog_review_list.append('null')  
            naver_map_type_list.append('null')
            blog_review_qty_list.append('null')
            
    driver.quit()
    
    
    df['naver_store_type'] = naver_map_type_list  # 네이버 상세페이지에서 크롤링한 업체 유형
    df['naver_blog_review_qty'] = blog_review_qty_list  # 네이버 상세페이지에 나온 블로그 리뷰의 총 개수
    
    df['naver_blog_review_qty'] = df['naver_blog_review_qty'].str.replace(',', '').astype(float)
    
    # 별점 평균, 수 같은 데이터 역시 스트링 타입으로 크롤링이 되었으므로 numeric으로 바꿔줍니다.
    df['naver_blog_review_qty'] = df['naver_blog_review_qty'].apply(pd.to_numeric)
    
    df = df.replace('null', 0)
    df['naver_blog_review_qty'] = df['naver_blog_review_qty'].str.replace(',', '').astype(float)
    df['naver_blog_review_qty'] = df['naver_blog_review_qty'].apply(pd.to_numeric)

    df['naver_blog_review_qty'].mean()
    
    df.to_csv('중앙대-리뷰수.csv')
    return df



class CrollingNaver:
    def __init__(self, df):
        self.df = df
        self new_df = load_data(self.df)
        
        
    def loadCrollingData(self):
        return self.new_df
    
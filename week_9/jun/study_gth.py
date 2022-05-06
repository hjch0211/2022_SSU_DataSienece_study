# -*- coding: utf-8 -*-
"""
Created on Fri May  6 19:56:36 2022

@author: dali1
"""

import seaborn as sns
import pandas as pd
titanic = sns.load_dataset("titanic") #인자로 tiatanic 넣음
titanic.to_csv('C:/Users/dali1/OneDrive - 숭실대학교 - Soongsil University/2학년 1학기/데이터사이언스/titanic.csv', index= False) 
import matplotlib.pyplot as plt # 차트 그리기

# 결측값 채우기

print(titanic.isnull().sum())
titanic['age'] = titanic['age'].fillna(titanic['age'].median) # 중앙값으로 age 결측값 채우기
titanic['embarked'] = titanic['embarked'].fillna('S') #최빈값 S로 결측값 채우기 value_counts()로 확인할 수 있음
titanic['embark_town'] = titanic['embark_town'].fillna('Southampton') #최빈값으로 embark_town 채우기 value_counts()로 확인할 수 있음
titanic['deck'] = titanic['deck'].fillna('C') # 최빈값으로 deck 채우기... value_counts()로 확인할 수 있음
print(titanic.info())
print(titanic['survived'].value_counts())   ## titanic.survived 의 형식으로도 가능


# 남자 승객과 여자 승객의 생존율 pie 차트로 그리기
"""f,ax = plt.subplots(1,2, figsize=(10,5)) # 1행 2열짜리 만듦 .ax 는 각 축
titanic['survived'][titanic['sex']=='male'].value_counts().plot.pie(explode=[0,0.1], autopct = '%1.1f%%',ax=ax[0], shadow= True) # 남자
titanic['survived'][titanic['sex']=='female'].value_counts().plot.pie(explode=[0,0.1], autopct = '%1.1f%%',ax=ax[1], shadow= True) # 남자
ax[0].set_title('Survived Male')
ax[1].set_title('Survived Female')
plt.show()
"""

# 등급별 생존자수를 차트로 나타내기
"""
sns.countplot('pclass',hue ='survived', data = titanic)
plt.title('Pclass vs Survived')
plt.show()
"""

# 이제 상관계수를 그려보자
"""
titanic_corr = titanic.corr(method = 'pearson')
print(titanic_corr)
titanic_corr.to_csv('C:/Users/dali1/OneDrive - 숭실대학교 - Soongsil University/2학년 1학기/데이터사이언스/titanic_Corr.csv', index= False)
"""

#특정 변수 사이의 상관계수 구하기 즉 한개만 뽑기 
"""
print(titanic['survived'].corr(titanic['adult_male'])) ##생존과 성인 남자와의 관계. -0.5577
print(titanic['survived'].corr(titanic['fare']))

"""
#상관 분석 시각화하기
titanic['adult_male'] = titanic['adult_male'].astype(int) ##pariplot에서 bool값을 못읽음
titanic['alone'] = titanic['alone'].astype(int) ##pariplot에서 bool값을 못읽음
sns.pairplot(titanic, hue= 'survived')
plt.title('test')
plt.show()


#두 변수만 상관분석 시각화
"""
sns.catplot(x='pclass',y='survived', hue='sex', data=titanic, kind='point')
plt.show()
"""

#변수 사이의 상관계수를 히트맵으로 표현. 교수님 방식
"""
sns.heatmap(titanic.corr(method ='pearson'), annot = True)
plt.show()
"""





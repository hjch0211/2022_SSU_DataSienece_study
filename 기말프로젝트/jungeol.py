# -*- coding: utf-8 -*-
"""



"""

import pandas as pd

def load_data(univ):
    excel_data = pd.read_csv("대학리스트.csv")
    result_data= excel_data[excel_data['대학']==univ]
    return str(result_data['시군구코드'].values[0]), result_data['행정동이름'].values[0]

def load_xy(univ):
    excel_data = pd.read_csv("대학리스트.csv")
    result_data= excel_data[excel_data['대학']==univ]
    return str(result_data['경도'].values[0]), result_data['위도'].values[0]

    
    
def main():
    a, b = load_data('숭실대학교')
    print(type(str(a)))
    print(type(b))


    
if __name__ =='__main__':
    main()



class LoadUnivData:
    def __init__(self, univ):
        self.univ = univ
        self.gucode, self.dongname = load_data(self.univ)
        self.cx, self.cy = load_xy(self.univ)
        
        
    def loadUniv(self):
        return self.gucode, self.dongname
    
    def loadXY(self):
        return self.cx, self.cy
        
        
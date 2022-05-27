# -*- coding: utf-8 -*-
"""
Created on Fri May 27 22:07:32 2022

@author: dali1
"""

import json

with open('.\resourse\서울시 우리마을가게 상권분석서비스(상권-소득소비).json','r') as f:
    json_data = json.load(f)
print(json.dumps(json_data))
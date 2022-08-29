from selenium import webdriver
from openpyxl import Workbook
import time
import re
import numpy as np
import pandas as pd
from selenium.webdriver.common.keys import Keys
from sqlalchemy import false, true
import os
import pandas as pd

df_data = pd.DataFrame(columns=['accural_periodicity'])

'''크롬드라이버 경로 설정'''
driver = webdriver.Chrome('C:\\Users\\user\\Desktop\\python\\office_automation\\chromedriver.exe')


df = pd.read_csv('C://Users//user//Desktop//python//Public_data_collection//국성우_공공데이터_크롤링.csv', index_col = 0)
df['periodicity_ran_num'] = df['variable_url'].apply(lambda x: re.sub('[https://www.data.go.kr/data/|/fileData.do]', '', x))
# [] 쓰기, 써야지 정규식(|)이 먹힘
prd_list = list(df['periodicity_ran_num'])

periodicity_list = []

for i in prd_list:
    try:
        driver.get('https://www.data.go.kr/data/{}/fileData.do'.format(i))
        # driver.get('https://www.data.go.kr/data/{}/fileData.do'.format(prd_list[0]))
        driver.implicitly_wait(0.2)
        
        prd = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div[3]/div[5]/table/tbody/tr[8]/td').text
        
        # 뒤에 텍스트를 붙여야지 text만 빼올 수 있다.
        
        periodicity_list.append(prd)

    except:
        print('https://www.data.go.kr/data/{}/fileData.do'.format(i))
        
df_data['accural_periodicity'] = periodicity_list
print(df_data)

df_data.to_csv('test10.csv', index=false, encoding='utf-8-sig')
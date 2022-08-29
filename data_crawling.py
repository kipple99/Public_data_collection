import traceback
from selenium import webdriver
import time
import re
import numpy as np
import pandas as pd
from selenium.webdriver.common.keys import Keys
from sqlalchemy import false, true
import os
import pandas as pd
from bs4 import BeautifulSoup
import requests

df_data = pd.DataFrame(columns=['variable_url', 'title', 'periodicity'])


'''크롬드라이버 경로 설정'''
driver = webdriver.Chrome('C:\\Users\\user\\Desktop\\python\\office_automation\\chromedriver.exe')

driver.get('https://www.data.go.kr/tcs/dss/selectDataSetList.do?dType=FILE&keyword=&detailKeyword=&publicDataPk=&recmSe=&detailText=&relatedKeyword=&commaNotInData=&commaAndData=&commaOrData=&must_not=&tabId=&dataSetCoreTf=&coreDataNm=&sort=updtDt&relRadio=&orgFullName=&orgFilter=&org=&orgSearch=&currentPage=1&perPage=10&brm=&instt=&svcType=%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C&kwrdArray=&extsn=CSV&coreDataNmArray=&pblonsipScopeCode=')

variable_url_list = []
title_list = []
periodicity_list = []

for page_num in range(2, 3172):
    try:
        for i in range(1, 11):
            test = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[10]/div[2]/ul/li[{}]/dl/dt/a'.format(i))
            driver.execute_script('arguments[0].click();', test)

            variable_url = driver.current_url
            # print(variable_url)
            
            title = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div[1]/div[1]/p').text
            # print(title)
            # 뒤에 텍스트를 붙여야지 text만 빼올 수 있다.
            
            # periodicity = driver.find_element('/html/body/div[2]/div/div/div/div[2]/div[3]/div[6]/table/tbody/tr[8]/td').text
            response = requests.get(variable_url)
            rating_page = response.text
            soup = BeautifulSoup(rating_page, 'html.parser')
            periodicity = soup.find_all('td', 'td custom-cell-border-bottom')[7].text
            
            
            variable_url_list.append(variable_url)
            title_list.append(title)
            periodicity_list.append(periodicity)
            driver.back()
        
        '''홈페이지 연결'''
        driver.get('https://www.data.go.kr/tcs/dss/selectDataSetList.do?dType=FILE&keyword=&detailKeyword=&publicDataPk=&recmSe=&detailText=&relatedKeyword=&commaNotInData=&commaAndData=&commaOrData=&must_not=&tabId=&dataSetCoreTf=&coreDataNm=&sort=updtDt&relRadio=&orgFullName=&orgFilter=&org=&orgSearch=&currentPage={}&perPage=10&brm=&instt=&svcType=%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C&kwrdArray=&extsn=CSV&coreDataNmArray=&pblonsipScopeCode='.format(page_num))
        
        driver.implicitly_wait(3) # 1초안에 웹페이지를 load 하면 바로 넘어가거나, 1초를 기다림.
        print('정상적으로 진행중인 페이지:', page_num)

    
    except:
        print('오류 난 페이지:', page_num)
        print(traceback.format_exc())
        
df_data['variable_url'] = variable_url_list
df_data['title'] = title_list
df_data['periodicity'] = periodicity_list

print(df_data)
df_data.to_csv('국성우_공공데이터_크롤링.csv', index=false, encoding='utf-8-sig')
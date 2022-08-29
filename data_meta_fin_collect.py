import warnings
from logging.config import dictConfig
import logging
import inspect
import datetime
import traceback
from selenium import webdriver
import time
import re
import numpy as np
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import false, true
import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
''' log '''
warnings.filterwarnings(action = 'ignore') 
filePath = os.getcwd()
fileName = re.split('[\\\\|.]', inspect.getfile(inspect.currentframe()))[-2]
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s --- %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '{}\\logs\\{}_{}.log'.format(filePath, fileName, re.sub('-', '', str(datetime.date.today()))),
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
})
def log(msg):
    logging.info(msg)
''' main '''
# 수집용 데이터프레임
df_data = pd.DataFrame(columns=['variable_url', 'title', 'periodicity'])
# 크롬 드라이버 경로 설정
driver = webdriver.Chrome('C:\\Users\\user\\Desktop\\python\\office_automation\\chromedriver.exe')
driver.get('https://www.data.go.kr/tcs/dss/selectDataSetList.do?dType=FILE&keyword=&detailKeyword=&publicDataPk=&recmSe=&detailText=&relatedKeyword=&commaNotInData=&commaAndData=&commaOrData=&must_not=&tabId=&dataSetCoreTf=&coreDataNm=&sort=updtDt&relRadio=&orgFullName=&orgFilter=&org=&orgSearch=&currentPage=2001&perPage=10&brm=&instt=&svcType=%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C&kwrdArray=&extsn=CSV&coreDataNmArray=&pblonsipScopeCode=')
# url
variable_url_list = []
title_list = []
periodicity_list = []
# schema
name_list = []
description_list = []
url_list = []
keywords_list = []
license_list = []
dateCreated_list = []
dateModified_list = []
datePublished_list = []
creator_name_list = []
creator_contactType_list = []
creator_telephone_list = []
distribution_encodingFormat_list = []
distribution_contentUrl_list = []
for page_num in range(2001, 3400):
    try:
        log('#### Read Page {}'.format(page_num))
        for i in range(1, 11):
            try:
                # test = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[10]/div[2]/ul/li[{}]/dl/dt/a'.format(i))
                WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[10]/div[2]/ul/li[1]/dl/dt/a'))).click()
                # driver.execute_script('arguments[0].click();', test)
                variable_url = driver.current_url
                # log(variable_url)
                title = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div[1]/div[1]/p'))).text
                # title = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div[1]/div[1]/p').text
                # log(title)
                # 뒤에 텍스트를 붙여야지 text만 빼올 수 있다.
                # periodicity = driver.find_element('/html/body/div[2]/div/div/div/div[2]/div[3]/div[6]/table/tbody/tr[8]/td').text
                # collect periodicity by bs4
                response = requests.get(variable_url)
                rating_page = response.text
                soup = BeautifulSoup(rating_page, 'html.parser')
                periodicity = soup.find_all('td', 'td custom-cell-border-bottom')[7].text
                log('######## Collect \'{}\' : {}'.format(i, periodicity))
                variable_url_list.append(variable_url)
                title_list.append(title)
                periodicity_list.append(periodicity)
                #
                schema_url = re.sub('.do', '.json', re.sub('/data/', '/catalog/', variable_url))
                response = requests.get(schema_url)
                soup_dict = eval(response.text)
                # name_list.append(soup_dict['name'])
                description_list.append(soup_dict['description'])
                url_list.append(soup_dict['url'])
                keywords_list.append(soup_dict['keywords'][0])
                license_list.append(soup_dict['license'])
                dateCreated_list.append(soup_dict['dateCreated'])
                dateModified_list.append(soup_dict['dateModified'])
                datePublished_list.append(soup_dict['datePublished'])
                creator_name_list.append(soup_dict['creator']['name'])
                creator_contactType_list.append(soup_dict['creator']['contactPoint']['contactType'])
                creator_telephone_list.append(soup_dict['creator']['contactPoint']['telephone'].replace('+82-', ''))
                distribution_encodingFormat_list.append(soup_dict['distribution'][0]['encodingFormat'].lower())
                distribution_contentUrl_list.append(soup_dict['distribution'][0]['contentUrl'])
                driver.back()
            except:
                log('######## Collect \'{}\' : {} Error'.format(i, periodicity))
                log(traceback.format_exc())
        ''' 다음 페이지 이동 '''
        driver.get('https://www.data.go.kr/tcs/dss/selectDataSetList.do?dType=FILE&keyword=&detailKeyword=&publicDataPk=&recmSe=&detailText=&relatedKeyword=&commaNotInData=&commaAndData=&commaOrData=&must_not=&tabId=&dataSetCoreTf=&coreDataNm=&sort=updtDt&relRadio=&orgFullName=&orgFilter=&org=&orgSearch=&currentPage={}&perPage=10&brm=&instt=&svcType=%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C&kwrdArray=&extsn=CSV&coreDataNmArray=&pblonsipScopeCode='.format(page_num + 1))
        driver.implicitly_wait(3) # 1초안에 웹페이지를 load 하면 바로 넘어가거나, 1초를 기다림.
    except:
        log('############ Error Page : {}'.format(page_num))
        log(traceback.format_exc())
df_data['variable_url'] = variable_url_list
df_data['title'] = title_list
df_data['periodicity'] = periodicity_list
df_data['description'] = description_list
df_data['url'] = url_list
df_data['keywords'] = keywords_list
df_data['license'] = license_list
df_data['dateCreated'] = dateCreated_list
df_data['dateModified'] = dateModified_list
df_data['datePublished'] = datePublished_list
df_data['creator_name'] = creator_name_list
df_data['creator_contactType'] = creator_contactType_list
df_data['creator_telephone'] = creator_telephone_list
df_data['distribution_encodingFormat'] = distribution_encodingFormat_list
df_data['distribution_contentUrl'] = distribution_contentUrl_list
log(df_data)
df_data.to_csv('국성우_공공데이터_크롤링.csv', index=false, encoding='utf-8-sig')
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
df_data = pd.DataFrame(columns=['variable_url', 'title', 'periodicity', 'name', 'description', 'keywords', 'license', 'dateCreated', 'dateModified', 'datePublished', 'creator_name', 'creator_contactType', 'creator_telephone', 'distribution_encodingFormat', 'distribution_contentUrl'])
driver = webdriver.Chrome('C://Users//user//Desktop//python//office_automation//chromedriver.exe')
driver.get('https://www.data.go.kr/tcs/dss/selectDataSetList.do?dType=FILE&keyword=&detailKeyword=&publicDataPk=&recmSe=&detailText=&relatedKeyword=&commaNotInData=&commaAndData=&commaOrData=&must_not=&tabId=&dataSetCoreTf=&coreDataNm=&sort=&relRadio=&orgFullName=&orgFilter=&org=&orgSearch=&currentPage=3001&perPage=10&brm=&instt=&svcType=%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C&kwrdArray=&extsn=CSV&coreDataNmArray=&pblonsipScopeCode=')
collect_count = 3400 # 2001 ~ 3400
df_data = pd.DataFrame([], index = range(0, collect_count * 10))
col_list = ['variable_url', 'title', 'periodicity', 'description', 'keywords', 'license', 'dateCreated', 'dateModified', 'datePublished', 'creator_name', 'creator_contactType', 'creator_telephone', 'distribution_encodingFormat', 'distribution_contentUrl']
for col in col_list:
    df_data[col] = ''
for page_num in range(3001, collect_count): # 3001 ~ 3399
    try:
        for i in range(1, 11):
            try:
                # test = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[10]/div[2]/ul/li[{}]/dl/dt/a'.format(i))
                # driver.execute_script('arguments[0].click();', test)
                WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[10]/div[2]/ul/li[{}]/dl/dt/a'.format(i)))).click()
                # variable_url
                variable_url = driver.current_url
                # log(variable_url)
                # title
                title = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div[1]/div[1]/p').text
                # collect periodicity by bs4
                response = requests.get(variable_url)
                rating_page = response.text
                soup = BeautifulSoup(rating_page, 'html.parser')
                periodicity = soup.find_all('td', 'td custom-cell-border-bottom')[7].text
                log('######## Collect current_page : {} // \'{}\' : {} // periodicity : {}'.format(page_num, i, title, periodicity))
                # schema_url
                schema_url = re.sub('.do', '.json', re.sub('/data/', '/catalog/', variable_url))
                schema_response = requests.get(schema_url)
                soup_dict = eval(schema_response.text)
                # dataframe collect
                idx = (10 * page_num) + i - 11
                df_data.loc[idx, 'variable_url'] = variable_url
                df_data.loc[idx, 'title'] = title
                df_data.loc[idx, 'periodicty'] = periodicity
                df_data.loc[idx, 'description'] = soup_dict['description']
                df_data.loc[idx, 'keywords'] = soup_dict['keywords'][0]
                df_data.loc[idx, 'license'] = soup_dict['license']
                df_data.loc[idx, 'dateCreated'] = soup_dict['dateCreated']
                df_data.loc[idx, 'dateModified'] = soup_dict['dateModified']
                df_data.loc[idx, 'datePublished'] = soup_dict['datePublished']
                df_data.loc[idx, 'creator_name'] = soup_dict['creator']['name']
                df_data.loc[idx, 'creator_contactType'] = soup_dict['creator']['contactPoint']['contactType']
                df_data.loc[idx, 'creator_telephone'] = soup_dict['creator']['contactPoint']['telephone'].replace('+82-', '')
                df_data.loc[idx, 'distribution_encodingFormat'] = soup_dict['distribution'][0]['encodingFormat'].lower()
                df_data.loc[idx, 'distribution_contentUrl'] = soup_dict['distribution'][0]['contentUrl'] 
                driver.back()
            except:
                log('######## Collect // Error_page : {}  \'{}\' : {} // periodicity : {}'.format(page_num, i, title, periodicity))
                log(traceback.format_exc())
                driver.back()
        # 다음페이지 이동
        driver.get('https://www.data.go.kr/tcs/dss/selectDataSetList.do?dType=FILE&keyword=&detailKeyword=&publicDataPk=&recmSe=&detailText=&relatedKeyword=&commaNotInData=&commaAndData=&commaOrData=&must_not=&tabId=&dataSetCoreTf=&coreDataNm=&sort=updtDt&relRadio=&orgFullName=&orgFilter=&org=&orgSearch=&currentPage={}&perPage=10&brm=&instt=&svcType=%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C&kwrdArray=&extsn=CSV&coreDataNmArray=&pblonsipScopeCode='.format(page_num + 1))
        # driver.implicitly_wait(3) # 1초안에 웹페이지를 load 하면 바로 넘어가거나, 1초를 기다림.
    except:
        log('############ Error Page : {}'.format(page_num))
        log(traceback.format_exc())
        log('save_bkup // page : {}'.format(page_num))
        df_data.to_csv('백업데이터_국성우(에러페이지:{}).csv'.format(page_num))
df_data.to_csv('공공데이터수집(3001-3400)_국성우.csv', index=False, encoding='utf-8-sig')
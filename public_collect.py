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

driver.get('https://www.data.go.kr/tcs/dss/selectDataSetList.do?dType=FILE&keyword=&detailKeyword=&publicDataPk=&recmSe=&detailText=&relatedKeyword=&commaNotInData=&commaAndData=&commaOrData=&must_not=&tabId=&dataSetCoreTf=&coreDataNm=&sort=&relRadio=&orgFullName=&orgFilter=&org=&orgSearch=&currentPage=1&perPage=10&brm=&instt=&svcType=%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C&kwrdArray=&extsn=CSV&coreDataNmArray=&pblonsipScopeCode=')

collect_count = 3172

df_data = pd.DataFrame([], index = range(0, collect_count * 10))

col_list = ['variable_url', 'title', 'periodicity', 'description', 'keywords', 'license', 'dateCreated', 'dateModified', 'datePublished', 'creator_name', 'creator_contactType', 'creator_telephone', 'distribution_encodingFormat', 'distribution_contentUrl']

for col in col_list:
    df_data[col] = ''

for page_num in range(1, collect_count): # 3172
    try:
        for i in range(1, 11):
            test = driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[10]/div[2]/ul/li[{}]/dl/dt/a'.format(i))
            driver.execute_script('arguments[0].click();', test)
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
            log('######## Collect \'{}\' : {} // periodicity : {}'.format(i, title, periodicity))
            
            # schema_url
            schema_url = re.sub('.do', '.json', re.sub('/data/', '/catalog/', variable_url))
            schema_response = requests.get(schema_url)
            soup_dict = eval(schema_response.text)
            soup_dict_name = soup_dict['name']
            soup_dict_description = soup_dict['description']
            soup_dict_url = soup_dict['url']
            soup_dict_keywords = soup_dict['keywords']
            soup_dict_license = soup_dict['license']
            soup_dict_dateCreated = soup_dict['dateCreated']
            soup_dict_dateModified = soup_dict['dateModified']
            soup_dict_datePublished = soup_dict['datePublished']
            soup_dict_creator_name = soup_dict['creator']['name']
            soup_dict_creator_contactType = soup_dict['creator']['contactPoint']['contactType']
            soup_dict_creator_telephone = soup_dict['creator']['contactPoint']['telephone']     
            soup_dict_distribution_encodingFormat = soup_dict['distribution'][0]['encodingFormat']
            soup_dict_distribution_contentUrl = soup_dict['distribution'][0]['contentUrl']
            
            idx = (10 * page_num) + i - 11
            df_data.loc[idx, 'variable_url'] = variable_url
            # row_append
            # row_append = {
            #                 'variable_url': variable_url,
            #                 'title' : title,
            #                 'periodicity' : periodicity,
            #                 'name' : soup_dict_name,
            #                 'description' : soup_dict_description,
            #                 'url' : soup_dict_url,
            #                 'keywords' : soup_dict_keywords,
            #                 'license' : soup_dict_license,
            #                 'dateCreated' : soup_dict_dateCreated,
            #                 'dateModified' : soup_dict_dateModified,
            #                 'datePublished' : soup_dict_datePublished,
            #                 'creator_name' : soup_dict_creator_name,
            #                 'creator_contactType' : soup_dict_creator_contactType,
            #                 'creator_telephone' : soup_dict_creator_telephone,
            #                 'distribution_encodingFormat' : soup_dict_distribution_encodingFormat,
            #                 'distribution_contentUrl' : soup_dict_distribution_contentUrl
            #             }
            # df_data = df_data.append(row_append, ignore_index=True) 
            driver.back()
        
        # 다음페이지 이동
        driver.get('https://www.data.go.kr/tcs/dss/selectDataSetList.do?dType=FILE&keyword=&detailKeyword=&publicDataPk=&recmSe=&detailText=&relatedKeyword=&commaNotInData=&commaAndData=&commaOrData=&must_not=&tabId=&dataSetCoreTf=&coreDataNm=&sort=updtDt&relRadio=&orgFullName=&orgFilter=&org=&orgSearch=&currentPage={}&perPage=10&brm=&instt=&svcType=%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C&kwrdArray=&extsn=CSV&coreDataNmArray=&pblonsipScopeCode='.format(page_num + 1))
        driver.implicitly_wait(3) # 1초안에 웹페이지를 load 하면 바로 넘어가거나, 1초를 기다림.
                    
    except:
        pass

df_data.to_csv('테스트.csv', index=False, encoding='utf-8-sig')

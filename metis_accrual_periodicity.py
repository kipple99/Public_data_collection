import pandas as pd
import re
from urllib import response
import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

df_data = pd.DataFrame(columns=['accural_periodicity'])

df = pd.read_csv('C://Users//user//Desktop//python//Public_data_collection//국성우_공공데이터_크롤링.csv', index_col = 0)
df['periodicity_ran_num'] = df['variable_url'].apply(lambda x: re.sub('[https://www.data.go.kr/data/|/fileData.do]', '', x))
# [] 쓰기, 써야지 정규식(|)이 먹힘
random_num_list = list(df['periodicity_ran_num'])

periodicity_list = []

for i in random_num_list:
    try:
        url = 'https://www.data.go.kr/data/{}/fileData.do'.format(i)
        response = requests.get(url)
        rating_page = response.text
        soup = BeautifulSoup(rating_page, 'html.parser')
        prd = soup.find_all('td', 'td custom-cell-border-bottom')[7].text
        # 뒤에 '.text'를 붙이면 텍스트만 가져온다.
         
        periodicity_list.append(prd)
        print('.')
        
    except:
        print('https://www.data.go.kr/data/{}/fileData.do'.format(i))
        
        
df_data['accural_periodicity'] = periodicity_list
print(df_data)

df_data.to_csv('accural_periodicity.csv', index=False, encoding='utf-8-sig')
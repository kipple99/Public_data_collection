import pandas as pd
import re
from urllib import response
import requests
from bs4 import BeautifulSoup

df = pd.read_csv('C://Users//user//Desktop//python//Public_data_collection//국성우_공공데이터_크롤링.csv', index_col = 0)

df['schema_url'] = df['variable_url'].apply(lambda x:re.sub('.do', '.json', re.sub('/data/', '/catalog/', x)))

# lambda에서 x를 가공하고, 그 다음에 또 가공한 re.sub자체를 가공한다. 여기서, x는 한 데이터 프레임에 가공할 문자열(대상)을 의미한다.
# df.replace('https://www.data.go.kr/data/', '')가 안먹히는 이유? replace 메소드 자체가 선택적 값을 찾아서 해주는것이 아닌 값 자체(전체)를 치환해주는 것이기 때문에 re.sub 메소드를 사용해야한다.

url_list = list(df['schema_url'])
url_list = url_list
# url = url_list
# response = requests.get(url)
# soup_dict = eval(response.text)

col_list = ['name', 'description', 'url', 'keywords', 'license', 'dateCreated', 'dateModified', 'datePublished', 'creator_name', 'creator_contactType', 'creator_telephone', 'distribution_encodingFormat', 'distribution_contentUrl']

for col in col_list:
    df[col] = ''



for idx, url in enumerate(url_list):
    try:
        response = requests.get(url)
        soup_dict = eval(response.text)
        
        df.loc[idx, 'name'] = soup_dict['name']
        df.loc[idx, 'description'] = soup_dict['description']
        df.loc[idx, 'url'] = soup_dict['url']
        df.loc[idx, 'keywords'] = soup_dict['keywords']
        df.loc[idx, 'license'] = soup_dict['license']
        df.loc[idx, 'dateCreated'] = soup_dict['dateCreated']
        df.loc[idx, 'dateModified'] = soup_dict['dateModified']
        df.loc[idx, 'datePublished'] = soup_dict['datePublished']
        df.loc[idx, 'creator_name'] = soup_dict['creator']['name']
        df.loc[idx, 'creator_contactType'] = soup_dict['creator']['contactPoint']['contactType']
        df.loc[idx, 'creator_telephone'] = soup_dict['creator']['contactPoint']['telephone']
        df.loc[idx, 'distribution_encodingFormat'] = soup_dict['distribution'][0]['encodingFormat']
        df.loc[idx, 'distribution_contentUrl'] = soup_dict['distribution'][0]['contentUrl']
        
        print('.')
            
    except:
        print(url)
        pass
    
df.to_csv('공공데이터_정형.csv', encoding='utf-8-sig')
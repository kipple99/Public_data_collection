import pandas as pd
import re
from urllib import response
import requests
from bs4 import BeautifulSoup


df = pd.read_csv('국성우_공공데이터_크롤링.csv', index_col = 0)

df['schema_url'] = df['variable_url'].apply(lambda x:re.sub('.do', '.json', re.sub('/data/', '/catalog/', x)))

# lambda에서 x를 가공하고, 그 다음에 또 가공한 re.sub자체를 가공한다. 여기서, x는 한 데이터 프레임에 가공할 문자열(대상)을 의미한다.
# df.replace('https://www.data.go.kr/data/', '')가 안먹히는 이유? replace 메소드 자체가 선택적 값을 찾아서 해주는것이 아닌 값 자체(전체)를 치환해주는 것이기 때문에 re.sub 메소드를 사용해야한다.

schema_list = list(df['schema_url'])
print(schema_list)




# url = 'https://www.data.go.kr/catalog/15086316/fileData.json'
# response = requests.get(url)
# soup_dict = eval(response.text)

# print(soup_dict)

# for key in soup_dict.keys():
#     print(key)
    
# for value in soup_dict.values():
#     print(value)







for i in schema_list:
    try:
        url = i
        response = requests.get(url)
        soup_dict = eval(response.text)

        print(soup_dict)

        for key in soup_dict.keys():
            print(key)
            
        # key에 @달려있는건 가져오지 않기
        # 딕셔너리 안에 또 딕셔너리 가져오기
            
        for value in soup_dict.values():
            print(value)

        
    except:
        print('.')

import pandas as pd
import matplotlib.pyplot as plt
import requests
import re
from datetime import datetime
from matplotlib import dates as mdates
from bs4 import BeautifulSoup as bs

print('종목을 불러오고 있습니다...')
code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13')[0]
code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)
code_df = code_df[['회사명', '종목코드']]
stock_list = code_df.values.tolist()
print('종목을 불러왔습니다.')

tmp = input('종목 코드 혹은 이름을 입력하세요: ')
try:
    if re.match(r'^\d{6}$', tmp):
        code = tmp
        title = list(filter(lambda x: x[1] == code, stock_list))[0][0]
    else:
        code = list(filter(lambda x: x[0] == tmp, stock_list))[0][1]
        title = tmp
except IndexError:
    print('종목을 찾을 수 없습니다.')
    exit()

print(f'찾은 것: {title}({code})')

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}
df = pd.DataFrame()
sise_url = f'https://finance.naver.com/item/sise_day.nhn?code={code}'  
for page in range(1, 100):
    page_url = '{}&page={}'.format(sise_url, page)

    print(f'page: {page} / 99')

    # 위에서 했던 일련의 과정들을 각 url에 대해서 (99페이지에 대해서 반복)
    response = requests.get(page_url, headers=headers)
    html = bs(response.text, 'html.parser')
    html_table = html.select("table")
    table = pd.read_html(str(html_table))

    # 현재 얻은 데이터프레임을 기존 데이터프레임에 누적.
    df = df._append(table[0].dropna())

df = df.dropna()
df = df.iloc[0:30] 
df = df.sort_values(by='날짜')

plt.rc('font', family='Malgun Gothic')
plt.figure(figsize=(15, 5))
plt.title(title)
plt.xticks(rotation=45)
plt.plot(df['날짜'], df['종가'], 'co-')
plt.grid(color='gray', linestyle='--')
plt.show()
plt.savefig(f'{title}.png')
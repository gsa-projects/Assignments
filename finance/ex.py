import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime
from matplotlib import dates as mdates
from bs4 import BeautifulSoup as bs

code = input('종목 코드를 입력하세요: ')

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

plt.figure(figsize=(15, 5))
plt.title('Celltrion (close)')
plt.xticks(rotation=45)
plt.plot(df['날짜'], df['종가'], 'co-')
plt.grid(color='gray', linestyle='--')
plt.show()

plt.savefig('savefig_default.png')
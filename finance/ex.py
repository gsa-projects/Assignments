import requests
from bs4 import BeautifulSoup

def get_stock_info(stock_code):
    url = f'https://finance.naver.com/item/main.nhn?code={stock_code}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 종목명 가져오기
    stock_name = soup.select_one('div.wrap_company h2 a').text

    # 현재가 가져오기
    current_price = soup.select_one('p.no_today span.blind').text

    # 전일대비 가져오기
    change_price = soup.select_one('p.no_exday em em').text

    # 출력
    print(f'종목명: {stock_name}')
    print(f'현재가: {current_price}')
    print(f'전일대비: {change_price}')

# 예시로 삼성전자(005930)의 정보를 가져옴
get_stock_info('005930')

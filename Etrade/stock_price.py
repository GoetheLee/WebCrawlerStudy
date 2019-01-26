import pandas as pd
import urllib3,certifi
import matplotlib.pyplot as plt

class stock(object):
    def __init__(self):
        self.code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]

        self.code_df.종목코드 = self.code_df.종목코드.map('{:06d}'.format)
        self.code_df = self.code_df[['회사명', '종목코드']]
        self.code_df = self.code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})

    def get_code(self, item_name):
        code_df= self.code_df
        code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
        return code

    # 종목 이름을 입력하면 종목에 해당하는 코드를 불러와
    # 네이버 금융(http://finance.naver.com)에 넣어줌
    def get_url(self, item_name):
        code_df = self.code_df
        code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
        url = 'https://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)

        return url

    def get_stock_data(self, item_name,  n_pages=20):
        code_df = self.code_df
        url = get_url(item_name, code_df)

        #Force certificate check and use certifi to handle the certificate. 
        https = urllib3.PoolManager( cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where(),)  

        # 일자 데이터를 담을 df라는 DataFrame 정의
        df = pd.DataFrame()

        # 1페이지에서 20페이지의 데이터만 가져오기
        for page in range(1, n_pages + 1):
            pg_url = '{url}&page={page}'.format(url=url, page=page)
            #print('url: ', pg_url)
            https_url = https.urlopen('GET', pg_url) #' https://naver.com')  
            df = df.append(pd.read_html(https_url.data, header=0)[0], ignore_index=True)

        # df.dropna()를 이용해 결측값 있는 행 제거
        df = df.dropna()
        return df

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

    def get_url(self, item_name):
        code_df = self.code_df
        code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
        url = 'https://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)

        return url
    
    def pre_process(self, idf):
        pass

    def get_stock_data(self, item_name,  n_pages=20):
        code_df = self.code_df
        url = self.get_url(item_name)

        #Force certificate check and use certifi to handle the certificate. 
        https = urllib3.PoolManager( cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where(),)  

        df = pd.DataFrame()

        for page in range(1, n_pages + 1):
            pg_url = '{url}&page={page}'.format(url=url, page=page)
            #print('url: ', pg_url)
            https_url = https.urlopen('GET', pg_url) #' https://naver.com')  
            df = df.append(pd.read_html(https_url.data, header=0)[0], ignore_index=True)

        # df.dropna()를 이용해 결측값 있는 행 제거
        df = df.dropna()
        df['date'] = pd.to_datetime(df['날짜'])
        df = df.set_index('date')
        df = df.sort_index()
        return df

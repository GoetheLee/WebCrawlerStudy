import pandas as pd
import urllib3,certifi
import matplotlib.pyplot as plt

# import urllib
import time
import numpy as np
from itertools import repeat
import tqdm

from multiprocessing import Pool, cpu_count # Pool import하기

from urllib.request import urlopen
from bs4 import BeautifulSoup

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

        df = df.dropna()
        df['date'] = pd.to_datetime(df['날짜'])
        df = df.set_index('date')
        df = df.sort_index()
        return df
    
    def _get_stock_page(self, page, stockCode='035720'):
        url = 'http://finance.naver.com/item/frgn.nhn?code=' + stockCode + '&page=' + str(page)
        html = urlopen(url)

        source = BeautifulSoup(html.read(), "html.parser")
        dataSection = source.find("table", summary="외국인 기관 순매매 거래량에 관한표이며 날짜별로 정보를 제공합니다.")

        return pd.read_html( str( dataSection))[0].iloc[2:]
    
    def get_stock_parallel(self, name, n_pages=0):
        stockCode = self.get_code(name)
        print('stock code is : ', stockCode)
        trendOfInvestorUrl = 'http://finance.naver.com/item/frgn.nhn?code=' + stockCode
        trendOfInvestorHtml = urlopen(trendOfInvestorUrl)
        trendOfInvestorSource = BeautifulSoup(trendOfInvestorHtml.read(), "html.parser")

        trendOfInvestorPageNavigation = trendOfInvestorSource.find_all("table", align="center")
        trendOfInvestorMaxPageSection = trendOfInvestorPageNavigation[0].find_all("td", class_="pgRR")
        trendOfInvestorMaxPageNum = int(trendOfInvestorMaxPageSection[0].a.get('href')[-3:])
        print('Maximum page: ', trendOfInvestorMaxPageNum)
        if 0 == n_pages:
            n_pages = trendOfInvestorMaxPageNum

        cores = min(cpu_count(), n_pages)
        pages = [x for x in range(1, n_pages+1)]
        data_split = np.array_split(pages, cores)
        with Pool(cores) as pool:
            r = list(tqdm.tqdm(pool.starmap(self._get_stock_page, zip(pages, repeat(stockCode))), total=n_pages))
            df = pd.concat(r)
            pool.close()
            pool.join()
        cols = ['date', 'end_price', 'diff', 'diff_ratio', 'volume', 'institution', 'foriegn', 'foriegn_stocks', 'foriegn_occupy']
        df.columns = cols
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        df = df.sort_index()
        for col in [ 'end_price', 'diff', 'volume', 'institution', 'foriegn' ]:
            df[col] = df[col].map(lambda x: x.replace(',', ''))
            df[col] = df[col].astype('int32')
        for col in [ 'diff_ratio', 'foriegn_occupy']:
            df[col] = df[col].map(lambda x: x.replace('%', ''))
            df[col] = df[col].astype('float32')

        return df

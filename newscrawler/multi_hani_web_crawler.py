""" 
"""

import sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import argparse
import time

TARGET_URL_BEFORE_KEWORD = 'http://search.hani.co.kr/Search?command=query&' \
                           'keyword='
TARGET_URL_BEFORE_UNTIL_DATE = '&media=news&sort=s&period=all&datefrom=' \
                               '2000.01.01&dateto='
TARGET_URL_REST = '&pageseq='


def get_link_from_news_title(page_num, URL): #, output_file):
    res = []
    for i in range(page_num):
        URL_with_page_num = URL + str(i)
        source_code_from_URL = urllib.request.urlopen(URL_with_page_num)
        soup = BeautifulSoup(source_code_from_URL, 'lxml',
                             from_encoding='utf-8')        
        for item in soup.select('dt > a'):
            article_URL = item['href']
            res.append(article_URL)

    return res

def get_article_text(URL): #, output_file):
    source_code_from_url = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_url, 'html.parser', from_encoding='utf-8')
    content_of_article = soup.select('div.text')
    txt = ''
    for item in content_of_article:
        txt += item.get_text(strip=True) # str(item.find_all(text=True))
        
    return {'title': soup.title.string, 
            'datetime': [x.get_text() for x in soup.find('p', class_='date-time').contents],
            'subtitle':soup.find("div", attrs={'class': 'subtitle'}).get_text(',', strip=True), # [x for x in soup.find("div", attrs={'class': 'subtitle'}).contents],
            'contents': txt}


def main(args):
    start = time.perf_counter()
    keyword = args.key
    page_num = args.pagenum
    until_date = args.datetime
    #output_file_name = argv[4]
    target_URL = TARGET_URL_BEFORE_KEWORD + quote(keyword) \
                 + TARGET_URL_BEFORE_UNTIL_DATE + until_date + TARGET_URL_REST
    urls = get_link_from_news_title(page_num, target_URL)
    articles = []
    for url in urls:
        articles.append(get_article_text(url))
    with open('test.txt', 'wt') as f:
        for ar in articles:
            f.write(str(ar))
            f.write('\n\n')
    print('done!! time: ', time.perf_counter() - start)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", type=str, default='',
                    help="keyword for search")
    parser.add_argument("--pagenum", type=int, default=2,
                    help="crawl page number")
    parser.add_argument("--datetime", type=str, # default=2,
                    help="date for search")
    args = parser.parse_args()
    print(args)
    main(args)

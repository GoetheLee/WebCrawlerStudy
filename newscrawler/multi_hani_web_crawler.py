""" 한겨레 신문 특정 키워드를 포함하는, 특정 날짜 이전 기사 내용 크롤러(정확도순 검색)
    python [모듈이름] [키워드] [가져올 페이지 숫자] [가져올 기사의 최근 날짜]
    [결과 파일명.txt]
    한페이지에 10개
"""

import sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote

TARGET_URL_BEFORE_KEWORD = 'http://search.hani.co.kr/Search?command=query&' \
                           'keyword='
TARGET_URL_BEFORE_UNTIL_DATE = '&media=news&sort=s&period=all&datefrom=' \
                               '2000.01.01&dateto='
TARGET_URL_REST = '&pageseq='


def get_link_from_news_title(page_num, URL, output_file):
    for i in range(page_num):
        URL_with_page_num = URL + str(i)
        source_code_from_URL = urllib.request.urlopen(URL_with_page_num)
        soup = BeautifulSoup(source_code_from_URL, 'lxml',
                             from_encoding='utf-8')
        for item in soup.select('dt > a'):
            article_URL = item['href']
            get_text(article_URL, output_file)


def get_text(URL, output_file):
    source_code_from_url = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_url, 'lxml', from_encoding='utf-8')
    content_of_article = soup.select('div.text')
    for item in content_of_article:
        string_item = str(item.find_all(text=True))
        output_file.write(string_item)


def main(argv):
    if len(sys.argv) != 5:
        print("python [모듈이름] [키워드] [가져올 페이지 숫자] "
              "[가져올 기사의 최근 날짜] [결과 파일명.txt]")
        return
    keyword = argv[1]
    page_num = int(argv[2])
    until_date = argv[3]
    output_file_name = argv[4]
    target_URL = TARGET_URL_BEFORE_KEWORD + quote(keyword) \
                 + TARGET_URL_BEFORE_UNTIL_DATE + until_date + TARGET_URL_REST
    output_file = open(output_file_name, 'w')
    get_link_from_news_title(page_num, target_URL, output_file)
    output_file.close()


if __name__ == '__main__':
    main(sys.argv)

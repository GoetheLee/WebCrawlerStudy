

# from bs4 import BeautifulSoup4
from bs4 import BeautifulSoup
import urllib.request

# 출력 파일 명
OUTPUT_FILE_NAME = 'output.txt'
# 긁어 올 URL
# URL = 'http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=103&oid=055'\
#       '&aid=0000445667'

URL = 'http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=101&oid=421&aid=0002592830'


# 크롤링 함수
def get_text(URL):
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'lxml', from_encoding='utf-8')
    text = ''
    for item in soup.find_all('div', id='articleBodyContents'):
        text = text + str(item.find_all(text=True))
    return text


# 메인 함수
def main():
    open_output_file = open(OUTPUT_FILE_NAME, 'w')
    result_text = get_text(URL)
    open_output_file.write(result_text)
    open_output_file.close()


if __name__ == '__main__':
    main()



import urllib
# import requests
import time
 
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
  
stockItem = '035420' # naver
 
url = 'http://finance.daum.net/item/foreign_yyyymmdd.daum?page=1&code='+ stockItem
html = urlopen(url) 
# html = requests.get(url)
source = BeautifulSoup(html.read(), "html.parser")

# maxPage=source.find_all("table",align="center")
# mp = maxPage[0].find_all("td",class_="pgRR")
# mpNum = int(mp[0].a.get('href')[-3:])
mpNum = 20

for page in range(1, mpNum+1):
  print (str(page) )
  url = 'http://finance.daum.net/item/foreign_yyyymmdd.daum?page=' + str(page) + '&code=' + stockItem
  html = urlopen(url)
  source = BeautifulSoup(html.read(), "html.parser")
  srlists=source.find_all("tr")
  isCheckNone = None

  print(len(srlists))

  if((page % 1) == 0):
    time.sleep(1.50)

  for i in range(1,len(srlists)-1):
   if(srlists[i].span != isCheckNone):
     txt1 = srlists[i].get_text()
     print(txt1)

    #for(txt in srlists[i].find_all("td", class_="num").get_text())
    #  print(txt)
    #print(srlists[i].find_all("td", class_="num"))
    #srlists[i].td.text
    # print(srlists[i].find_all("td",class_="num cDn")[0].text)
#   print(srlists[i].find_all("td", class_="num")[0].text)
#    print(srlists[i].find_all("td",align="center")[0].text, srlists[i].find_all("td",class_="num")[0].text )

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
mpNum = 2

f = open("forigndata.txt", 'w')

for page in range(1, mpNum+1):
  print (str(page) )
  url = 'http://finance.daum.net/item/foreign_yyyymmdd.daum?page=' + str(page) + '&code=' + stockItem
  html = urlopen(url)
  source = BeautifulSoup(html.read(), "html.parser")
  srlists=source.find_all("tr")
  isCheckNone = None

#  print(len(srlists))

  if((page % 1) == 0):
    time.sleep(1.50)

  for i in range(1,len(srlists)-1):
   if(srlists[i].span != isCheckNone):
     date1 = srlists[i].find_all("td", class_="datetime2")[0].text

     classnums = srlists[i].find_all("td", class_="num")
     forign_buy_amount = classnums[2].text
     organ_buy_amount = classnums[3].text
     endprice = classnums[4].text
     updownration = classnums[6].text
     data = date1 + "  " + forign_buy_amount + "  " + organ_buy_amount + \
            "  " + endprice + "  " + updownration + "\n"
     f.write(data)
     print("data: ", date1, "forign: ", forign_buy_amount, "organ: ", organ_buy_amount, "price: ", endprice, "scale: ", updownration)


     # print(srlists[i].find_all("td", class_="num").text())

    #for(txt in srlists[i].find_all("td", class_="num").get_text())
    #  print(txt)
    #print(srlists[i].find_all("td", class_="num"))
    #srlists[i].td.text
    # print(srlists[i].find_all("td",class_="num cDn")[0].text)
#   print(srlists[i].find_all("td", class_="num")[0].text)
#    print(srlists[i].find_all("td",align="center")[0].text, srlists[i].find_all("td",class_="num")[0].text )

f.close()
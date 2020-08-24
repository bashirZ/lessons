import requests
from lxml import etree
import lxml.html
import csv
import time

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36','accept':'*/*'}
HOST = 'https://stroymarket-05.ru'
  

def parse(url):
    try:
        api = requests.get(url, headers=HEADERS)
    except:
        return
    tree = lxml.html.document_fromstring(api.text)
    nazv = tree.xpath('//div[@class="item-title"]/a/span/text()')
    foto = tree.xpath('//img[@class="img-responsive "]/@src')
    with open("text.csv", "w", newline='') as csv_file:
        write = csv.writer(csv_file)
        for i in range (len(nazv)):
            write.writerow([nazv[i]])
            write.writerow([HOST+foto[i]])

def parse2(url):
    try:
        api = requests.get(url, headers=HEADERS)
    except:
        return
    tree = lxml.html.document_fromstring(api.text)
    nazv = tree.xpath('//div[@class="item-title"]/a/span/text()')
    foto = tree.xpath('//img[@class="img-responsive "]/@src')
    with open("text.csv", "a", newline='') as csv_file:
        write = csv.writer(csv_file)
        for i in range (len(nazv)):
            write.writerow([nazv[i]])
            write.writerow([HOST+foto[i]])

    


def main():
    url = "https://stroymarket-05.ru/catalog/04_ruchnoy_instrument/izmeritelnyy/lineyki_i_shchupy_izmeritelnye/?PAGEN_1={param}"
    
    parse("https://stroymarket-05.ru/catalog/04_ruchnoy_instrument/izmeritelnyy/lineyki_i_shchupy_izmeritelnye/")
    s = 2
    while s <=2:
        parse2(url.format(param=s))
        time.sleep(1)
        s += 1




if __name__ == "__main__":
    main()





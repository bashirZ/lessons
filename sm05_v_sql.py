import requests
from lxml import etree
import lxml.html
import sqlite3
import time

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36','accept':'*/*'}
HOST = 'https://stroymarket-05.ru'
  

def parse(url):
    try:
        api = requests.get(url, headers=HEADERS)
    except:
        return
    tree = lxml.html.document_fromstring(api.text)
    urls = tree.xpath('//div[@class="item-title"]/a/@href')

    return(urls)


def main():
    url = "https://stroymarket-05.ru/catalog/03_instrumenty_i_oborudovanie/kliningovoe_oborudovanie/moyki_vysokogo_davleniya/?PAGEN_1={param}"
    links = []
    s = 1
    while s <=2:
        urls = parse(url.format(param=s))
        for i in range (len(urls)):
            links.append(HOST + urls[i])
        
        time.sleep(1)
        s += 1
   
    args = []
    for link in links:
        api = requests.get(link, headers=HEADERS)
        tree = lxml.html.document_fromstring(api.text)
        name = tree.xpath('//*[@id="pagetitle"]/text()')
        foto = tree.xpath('//*[@id="photo-0"]/a/@href')
        
        foto = ''.join(foto)
        name = ''.join(name)
        foto_url = HOST + foto
        args.append((name, foto_url))
    
    conn = sqlite3.connect("mydata.db")
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO goods VALUES (?,?)", args)
    conn.commit()
    conn.close()



if __name__ == "__main__":
    main()





    


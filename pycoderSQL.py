import scrapy
import sqlite3
from urllib.parse import urljoin

HOST = 'https://stroymarket-05.ru'


class PycoderSpider(scrapy.Spider):
    name = "pycoder"
    start_urls = [
        'https://stroymarket-05.ru/catalog/02_elektrotovary/pribory_ucheta_i_izmereniya/',
    ]
    visited_urls = []



    def parse(self, response):
        if response.url not in self.visited_urls:
            self.visited_urls.append(response.url)
            for post_link in response.xpath('//div[@class="item-title"]/a/@href').extract():
                url = urljoin(response.url, post_link)
                yield response.follow(url, callback=self.parse_post)

            next_pages = response.xpath('//li[@class="flex-nav-next "]/a/@href').extract()
            next_page = next_pages[-1]

            next_page_url = urljoin(response.url+'/', next_page)
            yield response.follow(next_page_url, callback=self.parse)

    def parse_post(self, response):
        title = response.xpath('//h1/text()').extract()
        foto = response.xpath('//li[@id="photo-0"]/link/@href').extract()
    
        foto = ''.join(foto)
        title = ''.join(title)
        foto_url = HOST + foto
        
        args = []
        args.append((title, foto_url))
        
        conn = sqlite3.connect("mydata.db")
        cursor = conn.cursor()

        cursor.executemany("INSERT INTO goods VALUES (?,?)", args)
        conn.commit()
        conn.close()
        





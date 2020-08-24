from pycoder.items import PycoderItem
import scrapy
import csv
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
        item = PycoderItem()
        title = response.xpath('//h1/text()').extract()
        item['title'] = title
        foto = response.xpath('//li[@id="photo-0"]/link/@href').extract()
        item['foto'] = foto   
        yield item
        nazv = item ['title']
        foto_url = item ['foto']
        with open("text.csv", "a", newline='') as csv_file:
                write = csv.writer(csv_file)
                for i in range (len(nazv)):
                        write.writerow([nazv[i]])
                        write.writerow([HOST+foto_url[i]])


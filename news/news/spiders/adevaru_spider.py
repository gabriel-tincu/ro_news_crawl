import scrapy
from scrapy.linkextractors import LinkExtractor
import logging

class AdevarulSpider(scrapy.Spider):
    name = "adevarul"
    start_urls = [
        "http://adevarul.ro/"
    ]

    def parse(self, response):
        extractor = LinkExtractor(allow_domains=['www.adevarul.ro', 'adevarul.ro'])
        intro = response.css('#pagina-articol .articleOpening::text').extract_first()
        author = response.css('.a-name a::text').extract_first()
        if intro and author:
            author = author.strip()
            author = author.strip()
            tags = [x.strip() for x in response.css('.scolor a::text').extract()]
            date_ro = response.css('time::text').extract_first().strip()
            date_en = response.xpath('//meta[@http-equiv="last-modified"]/@content').extract_first().strip()
            title = response.css('h1::text').extract_first().strip()
            body = (x.strip() for x in response.css('#article-body div::text').extract())
            body = '\n'.join(x for x in body if x)
            data = {
                'url': response.url,
                'author': author,
                'date_ro': date_ro,
                'date_en': date_en,
                'tags': tags,
                'title': title,
                'intro': intro,
                'body': body,
                'type': 'adevarul'
            }
            doc_id = response.url.split('_')[-1]
            doc_id = doc_id.split('/')
            if len(doc_id) == 2 and 'index' in doc_id[1]:
                doc_id = doc_id[0]
            else:
                doc_id = response.url
            data['id'] = doc_id
            logging.info('got new document')
            yield data

        for link in extractor.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse)
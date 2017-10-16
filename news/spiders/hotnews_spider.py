from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor
import logging

logger = logging.getLogger('hotnews')

class HotnewsSpider(Spider):
    name = 'hotnews'
    start_urls = [
        'http://www.hotnews.ro/'
    ]

    def parse(self, response):
        extractor = LinkExtractor(allow_domains=['www.hotnews.ro', 'hotnews.ro'])
        title = response.css('h1::text').extract_first()
        author = response.css('.autor a::text').extract_first()
        tags = response.css('.atual::text').extract_first()
        date_ro = response.css('.data::text').extract_first()
        date_en = response.xpath('//meta[@name="DC.date.issued"]/@content').extract_first()
        intro = response.css('#articleContent strong::text').extract_first()
        body = response.css('#articleContent::text').extract()
        body = '\n'.join(x.strip() for x in body)
        if title and author and tags and body:
            tags = [x.lower().strip() for x in tags.split('|')]
            data = {
                'url': response.url,
                'author': author.strip(),
                'date_ro': date_ro.strip(),
                'date_en': date_en.strip() if date_en.strip() else '',
                'tags': tags,
                'title': title.strip(),
                'intro': intro.strip() if intro else '',
                'body': body,
                'type': 'hotnews',
                'id': response.url
            }
            yield data
        else:
            logger.info('could not id title, author, tags or body for doc {}'.format(response.url))
        for link in extractor.extract_links(response):
            yield Request(link.url, callback=self.parse)
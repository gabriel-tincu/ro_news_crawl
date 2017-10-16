from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor
import logging

logger = logging.getLogger('realitatea')


class RealitateaSpider(Spider):
    name = 'realitatea'
    start_urls = [
        'https://www.realitatea.net/'
    ]

    def parse(self, response):
        extractor = LinkExtractor(allow_domains=['www.realitatea.net', 'realitatea.net'])
        title = response.css('h1::text').extract_first()
        intro = response.css('.intro-2 p::text').extract_first()
        body = response.css('.article-ad+ p::text').extract()
        if title and body:
            body = [x.strip() for x in body]
            body = [x for x in body if x]
            data = {
                'url': response.url,
                'title': title.strip(),
                'intro': intro.strip() if intro else '',
                'body': '\n'.join(body),
                'type': 'realitatea',
                'id': response.url
            }
            yield data
        else:
            logger.info('could not id title,  tags or body for doc {}'.format(response.url))
        for link in extractor.extract_links(response):
            yield Request(link.url, callback=self.parse)
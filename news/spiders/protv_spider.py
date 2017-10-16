from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor
import logging

logger = logging.getLogger('protv')


class ProTVSpider(Spider):
    name = 'protv'
    start_urls = [
        'http://stirileprotv.ro'
    ]

    def parse(self, response):
        extractor = LinkExtractor(allow_domains=['stirileprotv.ro', 'www.stirileprotv.ro'])
        title = response.css('h1::text').extract_first()
        intro = response.css('.lead-articol p::text').extract_first()
        body = response.css('p::text').extract()
        tags = response.css('.author a::text').extract()
        if title and tags and body:
            body = [x.strip() for x in body]
            body = [x for x in body if x]
            data = {
                'url': response.url,
                'tags': tags,
                'title': title.strip(),
                'intro': intro.strip() if intro else '',
                'body': '\n'.join(body),
                'type': 'protv',
                'id': response.url
            }
            yield data
        else:
            logger.info('could not id title,  tags or body for doc {}'.format(response.url))
        for link in extractor.extract_links(response):
            yield Request(link.url, callback=self.parse)
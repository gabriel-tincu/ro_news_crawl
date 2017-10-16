from scrapy.linkextractors import LinkExtractor
import logging
import scrapy

logger = logging.getLogger('agerpres')

class AgerpressSpider(scrapy.Spider):
    name = 'agerpres'
    start_urls = [
        "http://www.agerpres.ro/"
    ]
    def parse(self, response):
        extractor = LinkExtractor(allow_domains=['www.agerpres.ro', 'agerpres.ro'])
        title = response.css('#body h1::text').extract_first()
        intro = response.css('.intro::text').extract_first()
        date_ro = response.css('.main time::text').extract_first()
        body = response.css('p::text').extract()

        if title and intro and date_ro and body:
            logger.info('indexing new doc with url {}'.format(response.url))
            body = [x.strip() for x in body]
            body = [x for x in body if x]
            tags = [x.strip() for x in response.css('.float a::text').extract()]
            tags = [x for x in tags if x]
            date_en = response.xpath('//time/@datetime').extract_first()
            data = {
                'url': response.url,
                'date_ro': date_ro.strip(),
                'date_en': date_en.strip(),
                'tags': tags,
                'title': title.strip(),
                'intro': intro.strip(),
                'body': '\n'.join(body),
                'type': "agerpres",
                'id': response.url
            }
            yield data
        else:
            logger.info('title, intro, date or body could not be matched for {}'.format(response.url))
        for link in extractor.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse)

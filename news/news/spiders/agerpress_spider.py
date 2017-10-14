from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor


class AgerpressSpider(Spider):
    name = 'agerpres'
    base_urls = [
        'https://www.agerpres.ro'
    ]

    def parse(self, response):
        extractor = LinkExtractor(allow_domains=['www.agerpres.ro', 'agerpres.ro'])
        title = response.css('h1::text').extract_first()
        intro = response.css('.intro::text').extract_first()
        date_ro = response.css('time::text').extract_first()
        body = [x.strip() for x in response.css('p::text').extract()]
        body = [x for x in body if x]
        tags = [x.strip() for x in response.css('.float a::text').extract()]
        tags = [x for x in tags if x]
        date_en = response.xpath('//time/@datetime').extract_first()
        if title and tags and intro and body:
            data = {
                'url': response.url,
                'date_ro': date_ro.strip(),
                'date_en': date_en.strip(),
                'tags': tags,
                'title': title.strip(),
                'intro': intro.strip(),
                'body': '\n'.join(body),
                'type': AgerpressSpider.name,
                'id': response.url
            }
            yield data
        for link in extractor.extract_links(response):
            yield Request(link.url, callback=self.parse)
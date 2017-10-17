import scrapy
from urllib.parse import (
    parse_qs,
    urlparse
)


class MagnetSpider(scrapy.Spider):
    start_urls = [
        ''
    ]
    allowed_domains = [
        ''
    ]

    def parse(self, response):
        links = [urlparse(x) for x in response.xpath('//a/@href').extract()]
        magnets = [parse_qs(x.query) for x in links if x.scheme == 'magnet']
        follows = [parse_qs(x.query) for x in links if x.scheme != 'magnet']
        yield magnets
        for x in follows:
            yield scrapy.Request(x, callback=self.parse)
from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor


class TVRSpider(Spider):
    name = 'tvr'
    base_urls = [
        'http://stiri.tvr.ro'
    ]

    def parse(self, response):
        extractor = LinkExtractor(allow_domains=['stiri.tvr.ro', 'tvr.ro'])
        tags = [x.strip() for x in response.css('.greyDark14::text').extract()]
        title = response.css('h1::text').extract_first()
        date_ro = response.css('.itemDate::text').extract_first()
        body = [x.strip() for x in response.css('p::text').extract()]
        date_en = response.xpath('//meta[@name="date"]/@content').extract_first()
        body = [x for x in body if x]
        if title and tags and body:
            date_ro = date_ro.strip().split('\n')[0]
            data = {
                'url': response.url,
                'date_ro': date_ro.strip(),
                'date_en': date_en.strip(),
                'tags': tags,
                'title': title.strip(),
                'body': '\n'.join(body),
                'type': TVRSpider.name,
                'id': response.url
            }
            yield data
        for link in extractor.extract_links(response):
            yield Request(link, callback=self.parse)
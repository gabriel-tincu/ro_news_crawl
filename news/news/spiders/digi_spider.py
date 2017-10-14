from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor


class DigiSpider(Spider):
    name = 'digi'
    base_urls = [
        'http://www.digi24.ro/'
    ]

    def parse(self, response):
        extractor = LinkExtractor(allow_domains=['www.digi24.ro', 'digi24.ro'])
        title = response.css('.h2::text').extract_first()
        intro = response.css('strong::text').extract_first()
        body = [x.strip() for x in response.css('.data-app-meta-article p::text').extract()]
        body = [x for x in body if x]
        date_ro = response.css('#itemprop-datePublished::text').extract_first()
        date_en = date_ro
        tags = [x.strip() for x in response.css('#itemprop-articleSection a::text').extract()]
        if title and tags and intro and body:
            data = {
                'url': response.url,
                'date_ro': date_ro.strip(),
                'date_en': date_en.strip(),
                'tags': tags,
                'title': title.strip(),
                'intro': intro.strip(),
                'body': '\n'.join(body),
                'type': 'digi',
                'id': response.url
            }
            yield data
        for link in extractor.extract_links(response):
            yield Request(link.url, callback=self.parse)
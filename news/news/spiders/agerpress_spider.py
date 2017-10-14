from scrapy.linkextractors import LinkExtractor
import scrapy


class AgerpressSpider(scrapy.Spider):
    name = 'agerpres'
    start_urls = [
        "http://agerpres.ro/"
    ]
    def parse(self, response):
        extractor = LinkExtractor(allow_domains=['www.agerpres.ro', 'agerpres.ro'])
        title = response.css('h1::text').extract_first()
        intro = response.css('.intro::text').extract_first()
        date_ro = response.css('time::text').extract_first()
        body = response.css('.mt35 p::text').extract()

        if title and intro and date_ro and body:
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
                'type': "foo",
                'id': response.url
            }
            yield data

        for link in extractor.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse)

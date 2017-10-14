from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor


class HotnewsSpider(Spider):
    name = 'hotnews'
    base_urls = [
        'http://www.hotnews.ro/'
    ]

    def parse(self, response):
        extractor = LinkExtractor(allow_domains=['www.hotnews.ro', 'hotnews.ro'])
        title = response.css('h1::text').extract_first()
        author = response.css('.autor a::text').extract_first()
        tags = [x.lower().strip() for x in response.css('.atual::text').extract_first().split('|')]
        date_ro = response.css('.data::text').extract_first()
        date_en = response.xpath('//meta[@name="DC.date.issued"]/@content').extract_first()
        intro = response.css('#articleContent strong::text').extract_first()
        body = response.css('#articleContent div+ div::text').extract()
        body = '\n'.join(x.strip() for x in body)
        if title and author and tags and intro and body:
            data = {
                'url': response.url,
                'author': author.strip(),
                'date_ro': date_ro.strip(),
                'date_en': date_en.strip(),
                'tags': tags,
                'title': title.strip(),
                'intro': intro.strip(),
                'body': body,
                'type': 'hotnews',
                'id': response.url
            }
            yield data
        for link in extractor.extract_links(response):
            yield Request(link.url, callback=self.parse)
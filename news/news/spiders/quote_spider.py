import scrapy

class QuoteSpider(scrapy.Spider):
    name = "quotes"
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = 'quotes-{}.html'.format(page)
        with open(filename, 'wb') as of:
            of.write(response.body)
        self.log('saved file {}'.format(filename))
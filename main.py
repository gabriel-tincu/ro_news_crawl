from scrapy.crawler import CrawlerProcess
from news.spiders.adevaru_spider import AdevarulSpider
from news.spiders.hotnews_spider import HotnewsSpider
from news.spiders.agerpress_spider import AgerpressSpider
from news.spiders.digi_spider import DigiSpider
from news.spiders.tvr_spider import TVRSpider
from news.spiders.protv_spider import ProTVSpider
from news.spiders.realitatea_spider import RealitateaSpider
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings

s = Settings()
s.setmodule('news.settings')

configure_logging(s)

process = CrawlerProcess(s)

process.crawl(AdevarulSpider)
process.crawl(RealitateaSpider)
process.crawl(ProTVSpider)
process.crawl(HotnewsSpider)
process.crawl(AgerpressSpider)
process.crawl(DigiSpider)
process.crawl(TVRSpider)

process.start()
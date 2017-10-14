from scrapy.crawler import CrawlerProcess
from news.news.spiders.adevaru_spider import AdevarulSpider
from news.news.spiders.hotnews_spider import HotnewsSpider
from news.news.spiders.agerpress_spider import AgerpressSpider
from news.news.spiders.digi_spider import DigiSpider
from news.news.spiders.tvr_spider import TVRSpider
import news.news.settings
from scrapy.utils.log import configure_logging

configure_logging()

process = CrawlerProcess()

process.crawl(AdevarulSpider)
process.crawl(HotnewsSpider)
process.crawl(AgerpressSpider)
process.crawl(DigiSpider)
process.crawl(TVRSpider)

process.start()
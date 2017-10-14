from scrapy.crawler import CrawlerProcess
from news.spiders.adevaru_spider import AdevarulSpider
from news.spiders.hotnews_spider import HotnewsSpider
from news.spiders.agerpress_spider import AgerpressSpider
from news.spiders.digi_spider import DigiSpider
from news.spiders.tvr_spider import TVRSpider

import news.settings as default_settings

from scrapy.utils.log import configure_logging
from scrapy.settings import Settings

s = Settings({
    'MONGO_URL': default_settings.MONGO_URL,
    'MONGO_COLLECTION': default_settings.MONGO_COLLECTION,
    'ITEM_PIPELINES': default_settings.ITEM_PIPELINES,
    'ES_URL': default_settings.ES_URL,
    'DOWNLOAD_DELAY': default_settings.DOWNLOAD_DELAY,
    'CONCURRENT_REQUESTS_PER_DOMAIN': default_settings.CONCURRENT_REQUESTS_PER_DOMAIN,
    'BOT_NAME': default_settings.BOT_NAME,
    'SPIDER_MODULES': default_settings.SPIDER_MODULES,
    'NEWSPIDER_MODULE': default_settings.NEWSPIDER_MODULE,
    'LOG_LEVEL': 'INFO'
})

configure_logging(s)

process = CrawlerProcess(s)

process.crawl(AdevarulSpider)
process.crawl(HotnewsSpider)
process.crawl(AgerpressSpider)
process.crawl(DigiSpider)
process.crawl(TVRSpider)

process.start()
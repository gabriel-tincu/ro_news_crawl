# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import logging
import elasticsearch


class NewsDuplicatePipeline:
    def __init__(self):
        self.id_set = set()

    def process_item(self, item, spider):
        try:
            if 'id' not in item or item['id'] in self.id_set:
                logging.error('dropping item with keys {}'.format(item.keys()))
                raise DropItem()
        except:
            raise DropItem()
        return item


class NewsESPipeline:
    def __init__(self, es_url, index_name):
        self.index_name = index_name
        self.doc_type = 'default'
        self.es_client = elasticsearch.Elasticsearch(hosts=[es_url])

    def process_item(self, item, spider):
        try:
            self.es_client.index(self.index_name, self.doc_type, item, item['id'])
            logging.info('successfully indexed doc with id {}'.format(item['id']))
        except Exception as e:
            logging.error('error indexing doc with id {}: {}'.format(item['id'], e))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
                crawler.settings.get('ES_URL', 'http://localhost:9200'),
                crawler.settings.get('ES_INDEX_NAME', 'default')
        )
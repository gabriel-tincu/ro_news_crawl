# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import logging
import elasticsearch
import pymongo


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

class NewsMongoPipeline:
    def __init__(self, mongo_url, collection_name):
        self.collection_name = collection_name
        self.mongo_client = pymongo.MongoClient(host=mongo_url)
        self.collection = self.mongo_client.get_database('default')[self.collection_name]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
                crawler.settings.get('MONGO_URL', '127.0.0.1'),
                crawler.settings.get('MONGO_COLLECTION', 'default')
        )

    def process_item(self, item):
        try:
            result = self.collection.insert_one(document=item)
            logging.info('added doc to mongodb {}'.format(result.inserted_id))
        except Exception as e:
            logging.error('error inserting item in mongo {}'.format(e))
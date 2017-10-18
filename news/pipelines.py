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
    def __init__(self, es_url, index_name):
        self.id_set = set()
        self.logger = logging.getLogger(__name__)
        self.logger.info('starting with es host {}'.format(es_url))
        self.es_client = elasticsearch.Elasticsearch(hosts=[es_url], http_auth=('elastic', 'changeme'))
        self.index_name = index_name
        self.doc_type = 'default'

    def has(self, item):
        return item['id'] in self.id_set or \
               self.es_client.exists(doc_type=self.doc_type, id=item['id'], index=self.index_name)

    def process_item(self, item, spider):
        if self.has(item):
            self.logger.info('skipping id {}'.format(item['id']))
            raise DropItem()
        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
                crawler.settings.get('ES_URL', 'http://localhost:9200'),
                crawler.settings.get('ES_INDEX_NAME', 'default')
        )


class NewsESPipeline:
    def __init__(self, es_url, index_name):
        self.logger = logging.getLogger(__name__)
        self.index_name = index_name
        self.doc_type = 'default'
        self.logger.info('starting with es host {}'.format(es_url))
        self.es_client = elasticsearch.Elasticsearch(hosts=[es_url], http_auth=('elastic', 'changeme'))

    def process_item(self, item, spider):
        if self.es_client.exists(doc_type=self.doc_type, id=item['id'], index=self.index_name):
            self.logger.info('skipping id {}'.format(item['id']))
            return
        try:
            self.es_client.index(self.index_name, self.doc_type, item, item['id'])
            self.logger.info('successfully indexed doc with id {}'.format(item['id']))
        except Exception as e:
            self.logger.error('error indexing doc with id {}: {}'.format(item['id'], e))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
                crawler.settings.get('ES_URL', 'http://localhost:9200'),
                crawler.settings.get('ES_INDEX_NAME', 'default')
        )


class NewsMongoPipeline:
    def __init__(self, mongo_url, collection_name):
        self.logger = logging.getLogger(__name__)
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
            self.logger.info('added doc to mongodb {}'.format(result.inserted_id))
        except Exception as e:
            self.logger.error('error inserting item in mongo {}'.format(e))
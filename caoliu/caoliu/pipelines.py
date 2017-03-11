# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from twisted.enterprise import adbapi
from datetime import datetime
# from hashlib import md5
import MySQLdb
import MySQLdb.cursors


class CaoliuPipeline(object):
    def process_item(self, item, spider):
        return item


class MySQLStorePipeline(object):
    def __init__(self):
        # self.conn = MySQLdb.connect('10.199.130.117', 'root', '123456', 'scrapy', charset="utf8", use_unicode=True)
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '123456', 'scrapy', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):    
        if item['title'] is not None:

            try:
                self.cursor.execute("""INSERT INTO caoliu (id, title, category, url)  
                                VALUES ('',%s, %s, %s)""", 
                                (item['title'], 
                                item['category'],
                                item['url']))

                self.conn.commit()


            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])


        # return item
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
# import json
# import codecs
from twisted.enterprise import adbapi
from datetime import datetime
# from hashlib import md5
import MySQLdb
import MySQLdb.cursors


class TianyaPipeline(object):
    def process_item(self, item, spider):
        return item



class MysqlPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', db='scrapy',user='root', passwd='123456', cursorclass=MySQLdb.cursors.DictCursor,charset='utf8', use_unicode=True)
    
    

    #pipeline默认调用
    def process_item(self, item, spider):

        d = self.dbpool.runInteraction(self._do_upinsert, item)
        print item['title']

        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d
    #将每行更新或写入数据库中
    def _do_upinsert(self, conn, item):
        print "99999999999999999999999999999999999999999999999999999999999999999999"
        # linkmd5id = self._get_linkmd5id(item)
        linkmd5id = 1
        
        
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        now = 1
        print item['content']
        print now
        sql = "insert into tianya(id,title,content,linkmd5id, create_time) values('','%s', '%s', %s, %d)"%(item['title'], item['content'], linkmd5id, now)
        print sql
        conn.execute(sql)

        # conn.execute("""
        #         select 1 from tianya where linkmd5id = %s
        # """, (linkmd5id, ))
        # ret = conn.fetchone()

        if ret:

            conn.execute("""
                update tianya set title = %s, description = %s, link = %s, listUrl = %s, updated = %s where linkmd5id = %s
            """, (item['title'], item['desc'], item['link'], item['listUrl'], now, linkmd5id))
            
            #print """
            #    update cnblogsinfo set title = %s, description = %s, link = %s, listUrl = %s, updated = %s where linkmd5id = %s
            #""", (item['title'], item['desc'], item['link'], item['listUrl'], now, linkmd5id)
        else:

            conn.execute("""
                insert into tianya(id,title,content,linkmd5id, create_time) 
                values('',%s, %s, %s, %s)
            """, (item['title'], item['content'], linkmd5id, now))
            
            #print """
            #    insert into cnblogsinfo(linkmd5id, title, description, link, listUrl, updated)
            #    values(%s, %s, %s, %s, %s, %s)
            #""", (linkmd5id, item['title'], item['desc'], item['link'], item['listUrl'], now)
    #获取url的md5编码
    # def _get_linkmd5id(self, item):
        #url进行md5处理，为避免重复采集设计
        # return md5(item['title']).hexdigest()
    #异常处理
    def _handle_error(self, failue, item, spider):
        log.err(failure)


class MySQLStorePipeline(object):
    def __init__(self):
        # self.conn = MySQLdb.connect('10.199.130.117', 'root', '123456', 'scrapy', charset="utf8", use_unicode=True)
        self.conn = MySQLdb.connect('127.0.0.1', 'root', '123456', 'scrapy', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):    
        if item['title'] is not None:

            try:
                self.cursor.execute("""INSERT INTO tianya (id, title, content, url)  
                                VALUES ('',%s, %s, %s)""", 
                                (item['title'].encode('utf-8'), 
                                item['content'].encode('utf-8'),
                                item['url'].encode('utf-8')))

                self.conn.commit()


            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])


        # return item
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class LagouPipeline(object):
    def process_item(self, item, spider):
        return item


class MySQLPipeline(object):
    '''
        将获取到的数据保存到MySQL数据库中
    '''
    def __init__(self, connect):
        self.connect = connect
        self.cursor = self.connect.cursor()

    @classmethod
    def from_settings(cls, settings):
        connect = pymysql.connect(host=settings['MYSQL_HOST'],
                                  db=settings['MYSQL_DBNAME'],
                                  user=settings['MYSQL_USERNAME'],
                                  passwd=settings['MYSQL_PASSWORD'],
                                  charset='utf8')
        return cls(connect)

    def process_item(self, item, spider):
        insert_sql = "insert into job(url, url_object_id, position, min_salary, max_salary, work_city, " \
                     "min_experience, max_experience, education, work_category, position_desc, workplace, " \
                     "company_name, company_url, publish_date) values(%s, %s, %s, %s, %s, %s, %s, %s, " \
                     "%s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(insert_sql, (item["url"], item["url_object_id"], item["position"], item["min_salary"],
                                         item["max_salary"], item["work_city"], item["min_experience"],
                                         item["max_experience"], item["education"], item["work_category"],
                                         item["position_desc"], item["workplace"], item["company_name"],
                                         item["company_url"], item["publish_date"]))
        self.connect.commit()

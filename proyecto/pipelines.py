# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
import MySQLdb

Conexion = MySQLdb.connect(host='localhost', user='conan', passwd='crom', db='Noticias')
micursor = Conexion.cursor(MySQLdb.cursors.DictCursor)

class NoticiasPipeline(object):

	#def __init__(self):

	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline

	def spider_opened(self, spider):
		query = ""

	def spider_closed(self, spider):
		micursor.close()
		Conexion.close()

	def process_item(self, item, spider):

		query = 'INSERT INTO Noticias (Enlace, Titulo, Fecha) VALUES (\''+item['enlace']+'\', \''+item['titulo']+'\', \''+item['fecha'][0:10]+'\');'

		micursor.execute(query)
		Conexion.commit()

		return item



#!/usr/bin/python
# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from proyecto.items import *

class NoticiasSpider(CrawlSpider):
	name = 'NoticiasSpider'
	allowed_domains = ['20minutos.es']
	start_urls = ['http://www.20minutos.es/']
	rules = (
		Rule(SgmlLinkExtractor(allow=(r'deportes/noticia/(\w|\d|-|/)*/', )), callback='parse_news', follow=False),
	)

	def parse_news(self, response):
		hxs = HtmlXPathSelector(response)
		elemento = Noticia()

		elemento['titulo'] = hxs.select('//h1[contains(@class, "article-title")]/text()')[0].extract()
		elemento['titulo'] = elemento['titulo'].encode('utf-8')
		elemento['fecha'] = hxs.select('//a[contains(@title, "Noticias del ")]/text()')[0].extract()
		elemento['fecha'] = elemento['fecha'].encode('utf-8')
		elemento['enlace'] = response.url

		return elemento



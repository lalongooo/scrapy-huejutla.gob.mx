from huejutlascrapy.items import HuejutlascrapyItem
from scrapy.selector import Selector
from scrapy.spiders import Spider
from scrapy.http import Request



url = "http://huejutla.gob.mx/web/Prensa.php?pag=%d"
starting_number = 1
number_of_pages = 108

class HuejutlaSpider(Spider):
	name = "huejutlaspider"
	allowed_domains = ["huejutla.gob.mx"]
	start_urls = [url % starting_number]

	def __init__(self):
		self.page_number = starting_number

	def start_requests(self):
		for i in range (self.page_number, number_of_pages, +1):
			yield Request(url = url % i, callback=self.parse)

	def parse(self, response):
		selectorResponse = Selector(response)
		sel = selectorResponse.xpath('//article')
		for s in sel:
			item = HuejutlascrapyItem()
			item["title"] = s.xpath('h2/text()').extract()
			item["desc"] = s.xpath('div/div[2]/p/text()').extract()
			item["link"] = s.xpath('footer/a/@href').extract()
			item["pub_date"] = str(s.xpath('div/div[2]/div/a[2]/text()').extract()).strip()
			item["number_read"] = str(s.xpath('div/div[2]/div/a[3]/text()').extract()).strip()
			yield item
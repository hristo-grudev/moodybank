import scrapy

from scrapy.loader import ItemLoader

from ..items import MoodybankItem
from itemloaders.processors import TakeFirst


class MoodybankSpider(scrapy.Spider):
	name = 'moodybank'
	start_urls = ['https://www.moodybank.com/news']

	def parse(self, response):
		post_links = response.xpath('//a[text()="Read More"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="blog-post-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="blog-post"]/span/text()').get()

		item = ItemLoader(item=MoodybankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

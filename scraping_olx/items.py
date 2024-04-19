# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapingOlxItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    price = scrapy.Field()
    negotiations = scrapy.Field()
    city = scrapy.Field()
    area = scrapy.Field()
    price_for_meter = scrapy.Field()
    link = scrapy.Field()
    text = scrapy.Field()



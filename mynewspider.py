import spiders.scrapy as scrapy


class MynewspiderSpider(scrapy.Spider):
    name = "mynewspider"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    def parse(self, response):
        pass

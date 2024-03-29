import scrapy

class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["www.rbye.vercel.app/"]
    start_urls = [
        "https://rbye.vercel.app/"
    ]

    def parse(self, response):
        # XPath를 사용하여 원하는 데이터 추출
        title = response.xpath('//title/text()').get()

        # 추출된 데이터 직접 출력
        print("--------------------------------")
        print(title)  
        print("--------------------------------")

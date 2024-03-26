import scrapy

class MyJobSpider(scrapy.Spider):
    name = 'myjobspider'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/jobs']

    def parse(self, response):
        for job in response.css('div.job_listing'):
            item = MyprojectItem()
            item['job_title'] = job.css('a::text').get()
            item['requirements'] = job.css('div.requirements::text').get()
            yield item

        # 다음 페이지 처리
        next_page = response.css('a.next_page::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

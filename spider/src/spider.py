import scrapy
from src.items import ScrapeResult


class WebSpider(scrapy.Spider):
    name = 'webspider'
    allowed_domains = ["google.com"]
    start_urls = ['https://www.google.com/']

    def parse(self, response):
        # follow pagination links
        for href in response.css('li.next a::attr(href)'):
            yield response.follow(href, self.parse)

        doc = ScrapeResult()
        doc['url'] = response.url
        doc['title'] = response.xpath('//div/p/text()').extract()
        doc['text'] = response.xpath('//body//p//text()').extract()
        yield doc  # Will go to the pipeline


from src.items import ScrapeResult
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class WebSpider(CrawlSpider):
    name = 'webspider'
    start_urls = ['https://swollwacht.nl/']
    allowed_domains = [x[x.index('//')+2:len(x)-1] for x in start_urls]
    print(allowed_domains)
    custom_settings = {
        'DEPTH_LIMIT': 1
    }
    rules = (
        Rule(LinkExtractor(allow_domains=allowed_domains, unique=True), callback='parse_item', follow=True),
    )

    @staticmethod
    def parse_item(response):
        doc = ScrapeResult()
        doc['url'] = response.url
        doc['title'] = response.xpath("//h1/text()").getall()
        doc['text'] = response.xpath('//body//p//text()').extract()
        yield doc

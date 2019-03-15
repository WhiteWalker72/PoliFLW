from src.scraper.items import ScrapeResult
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from src.persistence.sources_service import get_websites


class WebSpider(CrawlSpider):
    name = 'webspider'
    start_urls = list(filter(
        lambda x: x.lower().startswith('http') and len(x) > 0 and x.find('//') >= 0, get_websites()
    ))
    print(start_urls)
    allowed_domains = [x[x.index('//')+2:len(x)-1] for x in start_urls]

    # TODO: remove this line so the scraper will scrape all websites
    start_urls = ['https://swollwacht.nl/']
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

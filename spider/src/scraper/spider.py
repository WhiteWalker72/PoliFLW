from src.scraper.items import ScrapeResult
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from src.data.url_reader import websites
from src.producer import Producer

producer = Producer('unfiltered-articles-input')


class WebSpider(CrawlSpider):
    name = 'webspider'
    start_urls = []

    for website in websites:
        if len(website) > 0 and website.find('//') >= 0:
            start_urls.append(website)

    allowed_domains = [x[x.index('//')+2:len(x)-1] for x in start_urls]

    # TODO: remove this line so the scraper will scrape all websites
    start_urls = ['https://swollwacht.nl/']

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
        # producer.send_message(doc) TODO: fix this
        yield doc

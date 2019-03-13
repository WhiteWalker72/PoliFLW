from scrapy.crawler import CrawlerProcess
from src.scraper.spider import WebSpider
from src.scraper.pipelines import results


def main():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'ITEM_PIPELINES': {'src.scraper.pipelines.ResultPipeline': 4},
    })

    process.crawl(WebSpider)
    process.start()
    print(results)


if __name__ == "__main__":
        main()

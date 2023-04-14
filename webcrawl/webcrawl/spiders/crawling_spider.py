#reference: https://www.youtube.com/watch?v=m_3gjHGxIJc
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class WebCrawler(CrawlSpider):
    name = "WebCrawler" #identifier
    allowed_domains = ["ucr.edu"]
    start_urls = ["https://www.ucr.edu/"]

    rules = (
        Rule(LinkExtractor(allow=".edu")),
        Rule(LinkExtractor(allow=".gov")),
    )
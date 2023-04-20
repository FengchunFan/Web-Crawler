#reference: https://www.youtube.com/watch?v=m_3gjHGxIJc
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class WebCrawler(CrawlSpider):
    name = "WebCrawler" #identifier
    allowed_domains = ["ucr.edu",".gov"]
    start_urls = ["https://www.ucr.edu/", "https://news.ucr.edu/articles"]
    #crawl
    rules = (
        Rule(LinkExtractor(allow="articles"), callback="parse_articles"),
    )

    #decide how to scrape the links
    def parse_articles(self, response):
        yield{
            "title": response.css('meta[property="og:title"]::attr(content)').get(),
            "description": response.css('meta[property="og:description"]::attr(content)').get(),
            "url": response.css('meta[property="og:url"]::attr(content)').get()
        }
        
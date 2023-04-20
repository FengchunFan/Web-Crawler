#reference: https://www.youtube.com/watch?v=m_3gjHGxIJc
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider #stop spider under certain condition

class WebCrawler(CrawlSpider):
    name = "WebCrawler" #identifier
    allowed_domains = ["ucr.edu",".gov"]
    start_urls = ["https://www.ucr.edu/"]

    #testing purpose, remove later
    #for i in range(0,10):
    #    start_urls.append("https://news.ucr.edu/articles?page=" + str(i))

    #size limiter
    max_size = 0.1 * 1024 * 1024 #0.1MB => 102KB
    current_size = 0

    #crawl
    rules = (
        Rule(LinkExtractor(allow=".edu", deny="extension" and "collections/overview"), callback="parse"),
    #    Rule(LinkExtractor(allow="articles"), callback="parse"),
    #    Rule(LinkExtractor(allow="about"), callback="parse"),
    #    Rule(LinkExtractor(allow="research"), callback="parse"),
    )

    #decide how to scrape the links
    def parse(self, response):
        #specified by check source code for ucr webs
        title = response.css('meta[property="og:title"]::attr(content)').get() 
        description = response.css('meta[property="og:description"]::attr(content)').get()
        url = response.css('meta[property="og:url"]::attr(content)').get()
        # if none of the three field yield null and size is less than max_size
        if title and description and url and (self.current_size <= self.max_size): 
            temp_size = len(title) + len(description) + len(url)
            self.current_size = self.current_size + temp_size
            yield{
                "title": title,
                "description": description,
                "url": url
            }
        elif (self.current_size > self.max_size):
            raise CloseSpider

        # crawl urls from the current page, chatgpt generated code to recursively crawl
        for href in response.css('a::attr(href)').getall():
            if href.startswith('/'):
                yield response.follow(href, self.parse)
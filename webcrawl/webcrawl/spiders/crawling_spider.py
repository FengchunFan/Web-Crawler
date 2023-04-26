#reference: https://www.youtube.com/watch?v=m_3gjHGxIJc

#compile line: scrapy crawl WebCrawler -o output.json
#size check: stat -c "%s" output.json

import sys
import os
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
    max_size = 1 * 1024 * 1024 #0.1MB
    current_size = 0

    #crawl
    rules = (
        Rule(LinkExtractor(allow=".edu", deny="https://extension.ucr.edu/course"), callback="parse",), #can't figure these out yet
    #    Rule(LinkExtractor(allow="articles"), callback="parse"),
    )

    #decide how to scrape the links
    def parse(self, response):
        #force return type to be text, avoid scrapy.exceptions.NotSupported: Response content isn't text, chatgpt generated code
        #content_type = response.headers.get('content-type', '').decode('utf-8').lower()
        #if 'text/html' not in content_type:
        #    return

        #specified by check source code for ucr webs
        title = response.css('meta[property="og:title"]::attr(content)').get() 
        description = response.css('meta[property="og:description"]::attr(content)').get()
        url = response.css('meta[property="og:url"]::attr(content)').get()
        # if none of the three field yield null and size is less than max_size
        #if self.current_size <= self.max_size:
        
        if (title and url):
            yield{
               "title": title,
                "description": description,
                "url": url
            }

        if(os.path.isfile('output.json')):
            if(os.path.getsize('output.json') > self.max_size):
                print("reach size limit, size of output file: ", os.path.getsize('output.json')/1024/1024, "MB")
                raise CloseSpider

        #reference: https://www.youtube.com/watch?v=-mkewdn9JdU&t=415s
        for link in response.css('a::attr(href)').getall():
            if link.startswith('/'):
                yield response.follow(link, callback = self.parse)
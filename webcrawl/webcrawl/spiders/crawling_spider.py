#reference: https://www.youtube.com/watch?v=m_3gjHGxIJc

#compile line: scrapy crawl WebCrawler
#size check: stat -c "%s" output0.csv

import sys
import os
import csv
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider #stop spider under certain condition

class WebCrawler(CrawlSpider):
    name = "WebCrawler" #identifier
    allowed_domains = [".edu"]
    start_urls = ["https://www.ucr.edu/", "https://ucsd.edu/", "https://www.ucmerced.edu/", "https://uci.edu/", "https://www.ucdavis.edu/", "https://www.ucsc.edu/", "https://www.ucsb.edu/", "https://www.berkeley.edu/", "https://www.ucla.edu/"]

    #testing purpose, remove later
    #for i in range(0,10):
    #    start_urls.append("https://news.ucr.edu/articles?page=" + str(i))

    #size limiter
    max_size = 1 * 1024 * 1024 #1MB
    #current_size = 0
    document_num = 0
    file_name = f"output{document_num}.csv"
    
    #crawl
    rules = (
        Rule(LinkExtractor(allow=".edu"), callback="parse",), 
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
        #url = response.css('meta[property="og:url"]::attr(content)').get()
        url = response.url
        
        #as long as legit title and url
        if (title and url):
            yield{
               "title": title,
                "description": description,
                "url": url
            }
            data = [title, description, url]
            with open(self.file_name, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([item.replace('\n', '') for item in data]) #keep everything in 1 page 1 row format
                file.close()

        #size checker, making sure each output contains only the limited amount of data
        if(os.path.isfile(self.file_name)):
            if(os.path.getsize(self.file_name) > self.max_size):
                print("reach size limit, size of output file: ", os.path.getsize(self.file_name)/1024/1024, "MB")
                self.document_num += 1
                self.file_name = f"output{self.document_num}.csv"
                #raise CloseSpider

        if(self.document_num == 2):
            raise CloseSpider

        #reference: https://www.youtube.com/watch?v=-mkewdn9JdU&t=415s
        for link in response.css('a::attr(href)').getall():
            #if link.startswith('/') and 'program/finder' not in link and 'about/news' not in link:
            if link.startswith('/') and "edu" in link:
                yield response.follow(link, callback = self.parse)
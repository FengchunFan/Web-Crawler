#scrapy crawl HotelCrawler -o output.json

import sys
import os
import csv
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider #stop spider under certain condition

class HotelCrawler(CrawlSpider):
    name = "HotelCrawler" #identifier
    allowed_domains = ["www.hotels.com"]
    #allowed_domains = [".edu", ".com"]
    #seed.txt, to be modified
    start_urls = ["https://www.hotels.com/"]
    
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
        title_plain = response.css('title::text').get()
        title_og = response.css('meta[property="og:title"]::attr(content)').get() 
        description_meta = response.css('meta[name="Description"]::attr(content)').get()
        description_og = response.css('meta[property="og:description"]::attr(content)').get()
        #url = response.css('meta[property="og:url"]::attr(content)').get()
        url = response.url #url of current website
        
        if (title_og):
            title = title_og
        else:
            title = title_plain
        
        if(description_og):
            description = description_og
        else:
            description = description_meta

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

        #reference: https://www.youtube.com/watch?v=-mkewdn9JdU&t=415s
        for link in response.css('a::attr(href)').getall():
            #if link.startswith('/') and 'program/finder' not in link and 'about/news' not in link:
            if link.startswith('/') and "edu" in link:
                yield response.follow(link, callback = self.parse)
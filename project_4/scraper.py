import logging
import re
import string
import os.path
from abc import ABC

from nltk import word_tokenize
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ConcordiaScraper(CrawlSpider, ABC):
    """
    This is the SCRAPY class. It takes CRAWLSPIDER and ABC as parameters. To run this alone we have to use
    "scrapy ...." command. So a class was added bellow to run as Python Script.

    The scraper's name is "concordia", the only allowed domain in "concordia.ca".

    Rules are set to disable subdomains which carried a significant amount of useless information found on the original
    Concordia domain.

    parse_item() is the scraper function, only the first <section> in the first <div> in <body> tag is extracted since
    footer and header contain useless information not needed for the purposes of this PROJECT.
    BS$ is used to extract the text and NLTK for tokenization. The text is then cleaned from punctuations and
    case folded.
    """
    name = "concordia"
    logging.getLogger('scrapy').propagate = False
    start_urls = [
        'https://concordia.ca/',
    ]
    scraped_urls = []
    allowed_domains = ['concordia.ca']
    rules = (
        Rule(LinkExtractor(deny=(r'(^(?!https://www.concordia.ca).+)|(^(https://www.concordia.ca/fr/))|(^('
                                 r'https://www.concordia.ca/news/authors/))',)),
             callback='parse_item', follow=True),
    )

    xpath_arguments = "//div/section"
    counter = 0

    def parse_item(self, response):
        clean_tokens = []
        url = f"{response.url}"
        self.scraped_urls.append(url)
        self.logger.info("Now Scrapping: {}".format(url))
        self.counter = self.counter + 1
        self.logger.info("Counter {}".format(self.counter))
        result = response.xpath(self.xpath_arguments).extract_first()
        if result is not None:
            soup = BeautifulSoup(result, "lxml")
            text = soup.get_text()
            tokens = word_tokenize(text)
            for token in tokens:
                if not re.fullmatch('[' + string.punctuation + ']+', token):
                    clean_tokens.append(token.lower())

        yield {
            "url": url,
            "content": clean_tokens,
        }

def start_crawl(limit):
    """
     This is just a helper method used to run Scrapy as a python script.
     It also contains the settings for Scrapy where we set "Depth_Priority" to 1 to achieve BFS.
     "CONCURRENT_REQUESTS" is set to 1 for my slow CPU, but it can be changed. Bare in mind that this might affect the
     limit of scraped URL's. For example if the limit is set at 5000, it might scape 5050 url's based on the number
     specified.
    """
    if os.path.isfile("result.json"):
        print("Removing old result file...")
        os.remove("result.json")
    process = CrawlerProcess(settings={
        "CONCURRENT_REQUESTS": 1,
        "DEPTH_PRIORITY": 1,
        "FEEDS": {
            'result.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 4,
                'item_export_kwargs': {
                    'export_empty_fields': True,
                },
            },
        },
        "LOG_LEVEL": 'INFO',
    })

    process.settings.set("ROBOTSTXT_OBEY", True)
    process.settings.set("CLOSESPIDER_ITEMCOUNT", limit)
    process.crawl(ConcordiaScraper)
    process.start()
    return ConcordiaScraper.scraped_urls

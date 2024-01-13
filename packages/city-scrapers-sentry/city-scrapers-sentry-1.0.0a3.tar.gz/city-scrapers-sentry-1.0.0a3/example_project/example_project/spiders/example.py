import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["www.example.com"]
    start_urls = ["https://www.example.com"]

    def parse(self, response):
        raise Exception("This is an example exception raised by city-scrapers-sentry")

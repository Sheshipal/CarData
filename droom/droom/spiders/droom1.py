import scrapy
from scrapy_splash import SplashRequest

class Droom1Spider(scrapy.Spider):
    name = 'droom1'
    allowed_domains = ['droom.in']
    # start_urls = ['https://droom.in/product/volkswagen-polo-highline12l-diesel-2012-60b675e157e5f8a2038b46e5']

    links = set()

    def start_requests(self):
        
        yield scrapy.Request(
            url="https://droom.in/product/volkswagen-polo-highline12l-diesel-2012-60b675e157e5f8a2038b46e5",
            callback = self.parse_details
        )

    def parse(self, response):
        #fetch the list of items
        list_of_items = response.xpath("//div[contains(@id, 'search_results')]/div")

        #extract a tags
        links = []
        for item in list_of_items:
            link = item.xpath(".//div[contains(@class, 'listing-item')]/div/a[contains(@href, 'https://droom.in/product')]/@href").extract_first()
            links.append(link)
        
        print(f"lenght of links : {len(links)}")
        print(f"links : {links}")

    def parse_details(self, response):
        data = response.xpath("//div[contains(@id, 'description')]").extract()

        print(data)
import scrapy
from scrapy_splash import SplashRequest

class Droom1Spider(scrapy.Spider):
    name = 'droom1'
    allowed_domains = ['droom.in']
    # start_urls = ['http://droom.in/cars/used?page=1&tab=grid&display_category=All+Cars&condition=used']

    def start_requests(self):
        yield SplashRequest(
            url="http://droom.in/cars/used?page=1&tab=grid&display_category=All+Cars&condition=used",
            callback = self.parse
        )
        pass

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
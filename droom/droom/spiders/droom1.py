import scrapy
from scrapy_splash import SplashRequest
from collections import defaultdict

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
        data = defaultdict(lambda:None)

        # extract name
        try:
            name = response.xpath("//div[contains(@class,'listing-card')]/h1/text()").extract_first()
            data['name'] = name
        except():
            name = None

        # extract price
        try:
            price = response.xpath("//div[text()='Selling Price']/parent::node()/div[not(contains(text(), 'Selling Price'))]/text()").extract_first()
            data['price'] = price
        except():
            price = None

        try:
            # extract summary block
            summary = response.xpath("//div[contains(@class ,'product-summery')]")

            # get div blocks in summary
            blocks = summary[0].xpath(".//div/div") 
            product_summary = blocks[0]
            tech_specs = blocks[1]
            
            # get li elements in block0
            product_details = product_summary.xpath("//div/h2[text()= 'Product Summary']/parent::node()/div/ul/li/div/text()").extract()
            
            # get li elements in block1
            tech_specifications = tech_specs.xpath("//div/h2[contains(text(),'Tech Specs')]/parent::node()/div/ul/li/div/text()").extract()
            specifications = []
            for specification in tech_specifications:
                data = specification.strip()
                if len(data) > 0:
                    specifications.append(data)

            # seperete data
            data['owner'] = product_details[0]
            data['driven km'] = product_details[1]
            data['transmission'] = product_details[2]
            data['fuel'] = product_details[3]
            data['body type'] = product_details[4]
            data['mileage'] = specifications[0]
            data['engine cc'] = specifications[1]
            data['max power bhp'] = specifications[2]
            data['wheel size inches'] = specifications[3]
            data['no of seats'] = specifications[4]
        except:
            pass

        print()

        yield {"data" : data}
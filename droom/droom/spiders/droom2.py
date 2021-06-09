import scrapy
import pandas as pd

class Droom2Spider(scrapy.Spider):
    name = 'droom2'
    allowed_domains = ['droom.in']
    # start_urls = ['http://droom.in/']

    data = pd.read_csv("links.csv")

    global links
    links = list(data["link"])
    
    def start_requests(self):
        # loop over the details pages
        for link in links:
            if len(link)>6:
                yield scrapy.Request(
                    url= link,
                    callback = self.parse
                )

    def parse(self, response):
        data = {}

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
                word = specification.strip()
                if len(word) > 0:
                    specifications.append(word)

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
        except():
            pass

        yield data
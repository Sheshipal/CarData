import scrapy

class Droom1Spider(scrapy.Spider):
    name = 'droom1'
    allowed_domains = ['droom.in']
    # start_urls = ['https://droom.in/product/volkswagen-polo-highline12l-diesel-2012-60b675e157e5f8a2038b46e5']


    def start_requests(self):
        number_of_pages = 100
        # loop over main pages
        for i in range(1,number_of_pages):
            url = f"https://droom.in/cars/used?page={i}&tab=grid&display_category=All+Cars&condition=used"
            yield scrapy.Request(
                url= url,
                callback = self.parse
            )

    def parse(self, response):
        #fetch the list of items
        list_of_items = response.xpath("//div[contains(@id, 'search_results')]/div")

        #extract a tags
        for item in list_of_items:
            link = item.xpath(".//div[contains(@class, 'listing-item')]/div/a[contains(@href, 'https://droom.in/product')]/@href").extract_first()
            if link:
                yield {"link" : link}
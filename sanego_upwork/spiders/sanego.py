import scrapy
import string


result = string.ascii_uppercase

# Printing the value
print(result)


class SanegoSpider(scrapy.Spider):
    name = 'sanego'
    allowed_domains = ['www.sanego.de']
    url_link = 'http://www.sanego.de/Arzt/'
    start_urls = ['http://www.sanego.de/Arzt/A',
                  'http://www.sanego.de/Arzt/B',
                  'http://www.sanego.de/Arzt/C',
                  'http://www.sanego.de/Arzt/C'
                  ]

    def parse(self, response):

        for href in response.xpath('//div[@class="content"]/ul/li/a/@href'):
            url = response.urljoin(href.extract())

            yield scrapy.Request(url, callback=self.parse_attr)

    def parse_attr(self, response):
        for links in response.xpath('//div[@class="rate"]/a/@href'):
            link = response.urljoin(links.extract())

            yield scrapy.Request(link, callback=self.parse_data)

    def parse_data(self, response):
        for details in response.xpath('//div[@id="doctorProfile"]'):
            if details.xpath('.//div[@class="article noBorder subscribeHeader"]/h1/text()').get() != "none":
                yield {
                    "Name": details.xpath('.//div[@class="article noBorder subscribeHeader"]/h1/text()').get(),
                    "Speciality": details.xpath('.//div[@class="content"]/ul[1]/li[1]/a[1]/font/font[1]/text()').get(),
                    "Phone Number": details.xpath('.//span[@class="fakeLink mobOnly"]/font/font/text()').get(),
                    "Language": details.xpath('.//div[@class="col-md-4"][2]/div/div/font[1]/font/text()').get()
                }
            elif details.xpath('.//div[@class="article noBorder subscribeHeader"]/h1/font/font[2]/text()').get() != "none":
                yield {
                    "Name": details.xpath('.//div[@class="article noBorder subscribeHeader"]/h1/font/font[2]/text()').get()
                }
            else:
                yield {
                    "Name": details.xpath('.//div[@class="article noBorder subscribeHeader"]/h1/font/font/text()').get()
                }

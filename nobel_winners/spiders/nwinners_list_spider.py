import scrapy
import re


# Define the data to be scraped
class NWinnterItem(scrapy.Item):
    country = scrapy.Field()
    name = scrapy.Field()
    link_text = scrapy.Field()


# Create a named spider
class NWinnerSpider(scrapy.Spider):
    """ This spider scrapes the country and link-text of the Nobel winners """

    name = 'nwinners_list'
    allowed_domains = ['en.wikipedia.org']
    start_urls = [
        "https://en.wikipedia.org/wiki/List_of_Nobel_laureates_by_country"
    ]

    # Parse method to deal with the HTTP requests

    def parse(self, response):

        # Get all of the <h2> in the document
        h2s = response.xpath('//h2')

        for h2 in h2s:
            country = h2.xpath('span[@class="mw-headline"]/text()').extract()
            if country:
                winners = h2.xpath('following-sibling::ol[1]')[0]
                for w in winners.xpath('li'):
                    text = w.xpath('descendant-or-self::text()').extract()
                    yield NWinnterItem(
                        country=country[0],
                        name=text[0],
                        link_text=' '.join(text)
                    )
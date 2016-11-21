import scrapy
import re


# Define the data to be scraped
class NWinnterItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    year = scrapy.Field()
    category = scrapy.Field()
    country = scrapy.Field()
    gender = scrapy.Field()
    born_in = scrapy.Field()
    date_of_birth = scrapy.Field()
    date_of_death = scrapy.Field()
    place_of_birth = scrapy.Field()
    place_of_death = scrapy.Field()
    text = scrapy.Field()


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
            if len(h2.xpath('span[@class="mw-headline"]/text()')) == 0:
                h2s.remove(h2)

        while len(h2s[0].xpath('span[@id="Argentina"]/text()')) == 0:
            h2s.remove(h2s[0])

        while len(h2s[len(h2s) - 1].xpath('span[@id="Yugoslavia"]/text()')) == 0:
            h2s.remove(h2s[len(h2s) - 1])

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
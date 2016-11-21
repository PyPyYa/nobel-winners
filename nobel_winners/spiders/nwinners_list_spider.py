import scrapy
import re

BASE_URL = 'http://en.wikipedia.org'


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
                for winner in winners.xpath('li'):
                    winner_data = process_winner_li(winner, country[0])
                    yield  NWinnterItem(winner_data)
                    # yield NWinnterItem(
                    #     country=country[0],
                    #     name=text[0],
                    #     link_text=' '.join(text)
                    # )


def process_winner_li(winner, country=None):
    """
    Process a winner's <li> tag, adding country of birth or nationality,
    as applicable
    :param winner: <li> selector of winner
    :param country: country under which winner is found
    :return: processed winner data object
    """

    winner_data = {}

    link = winner.xpath('a/@href').extract()[0]

    if link:
        winner_data['link'] = BASE_URL + link

    text = winner.xpath('descendant-or-self::text()').extract()

    if text:
        text = ' '.join(text)
        # We expect the first element of the list in text to be the name
        name = text.split(',')[0].strip()
        if name:
            winner_data['name'] = name

        year = re.findall('\d{4}', text)
        if year:
            winner_data['year'] = int(year[0])
        else:
            winner_data['year'] = 0
            print('Oops, no year in ', text)

        category = re.findall('Physics|Chemistry|Physiology or Medicine|Literature|Peace|Economics', text)
        if category:
            winner_data['category'] = category[0]

        if country:
            if text.find('*') != -1:
                winner_data['country'] = ''
                winner_data['born_in'] = country
            else:
                winner_data['country'] = country
                winner_data['born_in'] = ''

        winner_data['text'] = text

    print(winner_data)
    return winner_data

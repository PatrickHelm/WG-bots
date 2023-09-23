import scrapy

class QuotesSpider(scrapy.Spider):
    name = "wg-gesucht"
    start_urls = [
                'https://www.wg-gesucht.de/wg-zimmer-in-Muenchen.90.0.1.0.html?offer_filter=1&city_id=90&sort_order=0&noDeact=1&dFr=1701428400&categories%5B%5D=0&rent_types%5B%5D=2&rMax=700&sin=1&exc=2',
            ]

    def parse(self, response):
        for quote in response.css('h3.truncate_title a::attr(href)').extract():
            if 'airbnb.pvxt.net' in quote or 'housinganywhere.com' in quote or 'roomlessrent' in quote or 'asset_id' in quote:
                pass
            else:
                yield {
                    "data-id": quote
                        }

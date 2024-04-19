import scrapy


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["olx.pl"]
    start_urls = ["https://www.olx.pl"]
    custom_settings = {
        'USER_AGENT':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_url = 'https://www.olx.pl'

    def parse(self, response, **kwargs):
        list_of_cites = ['grodzisk-mazowiecki', 'warszawa']
        search_radius = '100'  # in kilometers
        max_price = '2000000'
        url = ((self.start_url + '/nieruchomosci/dzialki/sprzedaz/' + list_of_cites[1] + '/?search%5Bdist%5D=' +
               search_radius) + '&search%5Bfilter_float_price:to%5D=' + max_price +
               '&search%5Bfilter_enum_type%5D%5B0%5D=dzialki-budowlane&search%5Bfilter_enum_type%5D%5B1%5D=dzialki-rolno-budowlane')
        yield scrapy.Request(url, callback=self.parse_result)

    def parse_result(self, response):
        adverts = response.css('a.css-rc5s2u')
        for advert in adverts:
            link = advert.css('a.css-rc5s2u::attr(href)').get()
            if "www.otodom.pl" not in link:
                link = self.start_url + link

            city = advert.css('p.css-veheph::text').get()

            yield {
                'title': advert.css('h6.css-16v5mdi::text').get(),
                'price': advert.css('p.css-10b0gli::text').get(),
                'negotiations':  advert.css('span.css-1vxklie::text').get(),
                'city': city,
                'area': advert.css('span.css-643j0o::text').get().split('-')[0].strip(),
                'price_for_meter': advert.css('span.css-643j0o::text').get().split('-')[1].strip(),
                'link': link,
            }
        next_page = response.css(
            'a[data-testid="pagination-forward"][data-cy="pagination-forward"]::attr(href)').get()
        if next_page is not None:
            next_page_url = self.start_url + next_page
            yield response.follow(next_page_url, callback=self.parse_result)


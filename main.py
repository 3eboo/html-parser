import json
import os

from scrapy.crawler import CrawlerProcess
from scrapy.http import Response
from scrapy.spiders import Spider


class BookingSpider(Spider):
    name = 'booking'
    start_urls = [f'file://{os.path.abspath("task-booking.html")}']
    results = {}

    def parse(self, response: Response):
        self.results["title"] = response.css('#hp_hotel_name::text').get().strip()
        self.results["address"] = response.css('[data-node_tt_id="location_score_tooltip"]::text').get().strip()
        self.results["stars"] = response.css('.hp__hotel_ratings i::attr(class)').re_first('.*([0-5]+)')

        self.results["review_points"] = response.css('.average.js--hp-scorecard-scoreval::text').get()
        self.results["number_of_reviews"] = response.css('.trackit.score_from_number_of_reviews .count::text').get()

        self.results["description"] = '\n'.join(
            response.css('div.hotel_description_wrapper_exp p').xpath('string()').extract())
        self.results["room_categories"] = response.css('#maxotel_rooms .ftd').xpath('normalize-space(text())').extract()

        alternative_hotels = []
        for hotel in response.css('#althotelsRow td'):
            item = dict()
            item['link'] = hotel.css('td .althotel_link::attr(href)').get('')
            item['name'] = hotel.css('td .althotel_link::text').get('')
            item['rating'] = hotel.css('td .average.js--hp-scorecard-scoreval::text').get('')
            alternative_hotels.append(item)
        self.results["alternative_hotels"] = alternative_hotels

    def close(self, spider, reason):
        with open('output_data.json', 'w') as output_file:
            json.dump(self.results, output_file)

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(BookingSpider)
    process.start()

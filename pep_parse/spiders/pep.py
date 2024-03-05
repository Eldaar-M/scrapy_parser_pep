import scrapy

from pep_parse.constants import (
    ALLOWED_DOMAINS,
    PARSER_NAME,
    START_URLS
)
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = PARSER_NAME
    allowed_domains = [ALLOWED_DOMAINS]
    start_urls = [START_URLS]

    def parse(self, response):
        peps = response.css(
            'section#numerical-index td a::attr(href)'
        )
        for pep_link in peps:
            yield response.follow(
                pep_link,
                callback=self.parse_pep
            )

    def parse_pep(self, response):
        pep, number, dash, *name = response.css(
            'h1.page-title::text'
        ).get().split()
        data = {
            'number': number,
            'name': ' '.join(name).strip(),
            'status': response.css(
                'dt:contains("Status")+dd abbr::text'
            ).get(),
        }
        yield PepParseItem(data)

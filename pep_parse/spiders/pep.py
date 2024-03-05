import scrapy

from pep_parse.settings import (
    ALLOWED_DOMAIN,
    PARSER_NAME
)
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = PARSER_NAME
    allowed_domains = [ALLOWED_DOMAIN]
    start_urls = [f'https://{ALLOWED_DOMAIN}/']

    def parse(self, response):
        for pep_link in response.css(
            'section#numerical-index td a::attr(href)'
        ):
            yield response.follow(
                pep_link,
                callback=self.parse_pep
            )

    def parse_pep(self, response):
        pep, number, dash, *name = response.css(
            'h1.page-title::text'
        ).get().split()
        yield PepParseItem(
            dict(
                number=number,
                name=' '.join(name).strip(),
                status=response.css(
                    'dt:contains("Status")+dd abbr::text'
                ).get()
            )
        )

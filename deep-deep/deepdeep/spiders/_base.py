# -*- coding: utf-8 -*-
import csv
import io
import logging
import random
from typing import Optional

import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.utils.url import guess_scheme, add_http_if_no_scheme

from deepdeep.links import DictLinkExtractor
from deepdeep.downloadermiddlewares import offdomain_request_dropped


class BaseSpider(scrapy.Spider):
    """
    Base spider class with common code.

    Among other things it parses a file at ``seeds_url`` (URL per line)
    and calls parse for each URL.
    """

    seeds_url = None  # type: Optional[str]
    random_seed = 0
    response_count = 0
    initial_priority = 5

    # if you're using command-line arguments override this set in a spider
    # like this:
    # ALLOWED_ARGUMENTS = {'my_new_argument'} | BaseSpider.ALLOWED_ARGUMENTS
    ALLOWED_ARGUMENTS = {
        'seeds_url',
    }

    def __init__(self, *args, **kwargs):
        self._validate_arguments(kwargs)
        self.le = DictLinkExtractor()
        super().__init__(*args, **kwargs)

    def _validate_arguments(self, kwargs):
        for k in kwargs:
            if k not in self.ALLOWED_ARGUMENTS:
                raise ValueError(
                    "Unsupported argument: %s. Supported arguments: %r" % (
                        k, self.ALLOWED_ARGUMENTS)
                )

    def start_requests(self):
        if self.seeds_url is None:
            raise ValueError("Please pass seeds_url to the spider. It should "
                             "be a text file with urls, one per line.")
        seeds_url = guess_scheme(self.seeds_url)

        # crawer can randomize links to select; make crawl deterministic
        # FIXME: it doesn't make crawl deterministic because
        # scrapy is async and pages can be crawled in different order
        random.seed(int(self.random_seed))

        # don't log DepthMiddleware messages
        # see https://github.com/scrapy/scrapy/issues/1308
        logging.getLogger("scrapy.spidermiddlewares.depth").setLevel(logging.INFO)

        # increase response count on filtered out requests
        self.crawler.signals.connect(self.on_offdomain_request_dropped,
                                     offdomain_request_dropped)

        yield scrapy.Request(seeds_url, self._parse_seeds, dont_filter=True,
                             meta={'dont_obey_robotstxt': True})

    def _parse_seeds(self, response):
        for url, in csv.reader(io.StringIO(response.text)):
            if url == 'url':
                continue  # optional header
            url = add_http_if_no_scheme(url)
            yield scrapy.Request(url, self.parse, priority=self.initial_priority)

    def increase_response_count(self):
        """
        Call this method to increase response count and close spider
        if it is over a limit.

        This provides a more flexible alternative to default
        CloseSpider extension.
        """
        self.response_count += 1
        max_items = self.crawler.settings.getint('CLOSESPIDER_ITEMCOUNT',
                                                 float('inf'))
        if self.response_count >= max_items:
            raise CloseSpider("item_count")

    def on_offdomain_request_dropped(self, request):
        self.increase_response_count()
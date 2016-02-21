# -*-  coding: utf-8 -*-
"""
"""
import requests

from bilgic.providers.base import BaseProvider


class PexelsProvider(BaseProvider):
    
    BASE_URL = "http://api.pexels.com/v1/"
    SEARCH_URL = "{url}search?query={query}&per_page={per_page}"

    def __init__(self):
        self.headers = {"Authorization": ""}

    def set_credentials(self, api_key):
        self.headers["Authorization"] = api_key

    def _search(self, keyword):
        url = self.SEARCH_URL.format(query=keyword, url=self.BASE_URL, per_page=self.PER_PAGE)
        return requests.get(url, headers=self.headers).json()

    def _get_image_list(self, keyword):
        results = self._search(keyword)
        image_urls = []
        for photo in results['photos']:
            image_urls.append(photo['src']['tiny'])
        return image_urls


api = PexelsProvider()

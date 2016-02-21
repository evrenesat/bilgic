# -*-  coding: utf-8 -*-
"""
"""
import requests

from bilgic.providers.base import BaseProvider


class PixabayProvider(BaseProvider):
    SEARCH_URL = "https://pixabay.com/api/?key={api_key}&q={query}&per_page={per_page}"

    def set_credentials(self, api_key):
        self.api_key = api_key

    def _search(self, keyword):
        url = self.SEARCH_URL.format(query=keyword,
                                     api_key=self.api_key,
                                     per_page=self.PER_PAGE)
        return requests.get(url).json()

    def _get_image_list(self, keyword):
        results = self._search(keyword)
        image_urls = []
        for photo in results['hits']:
            image_urls.append(photo['webformatURL'].replace('_640', '_180'))
        return image_urls


api = PixabayProvider()

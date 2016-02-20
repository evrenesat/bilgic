# -*-  coding: utf-8 -*-
"""
"""
import base64

import requests

from bilgic.lib.cache import ImageContentCache, ImageSearchCache


class BaseProvider(object):
    def get_base64_image(self, url):
        image_cache = ImageContentCache(url.encode('base64'))
        return image_cache.get() or image_cache.set(base64.b64encode(requests.get(url).content))

    def get_image_list(self, keyword):
        cache = ImageSearchCache(keyword)
        return cache.get() or cache.set(self._get_image_list(keyword))

    def get_images(self, keyword, page=0, per_page=10):
        result_set = []
        for img_url in self.get_image_list(keyword)[per_page * page:(per_page * page + per_page)]:
            result_set.append(self.get_base64_image(img_url))
        return result_set

    def _get_image_list(self, keyword):
        # override this method
        pass

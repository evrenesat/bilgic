# -*-  coding: utf-8 -*-
"""
Base Cache object and some builtin subclasses of it.
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
import json

from pyoko.conf import settings
from redis import Redis

redis_host, redis_port = settings.REDIS_SERVER.split(':')
cache = Redis(redis_host, redis_port)

REMOVE_SCRIPT = """
local keys = redis.call('keys', ARGV[1])
for i=1, #keys, 5000 do
    redis.call('del', unpack(keys, i, math.min(i+4999, #keys)))
end
return keys
"""

_remove_keys = cache.register_script(REMOVE_SCRIPT)

class Cache(object):
    """
    Base cache object to implement specific cache object for each use case.

    Subclasses of this class can be consist of just a ```PREFIX``` attribute;

    .. code-block:: python

        class MyFooCache(Cache):
            PREFIX = 'FOO'

        # create cache object
        mycache = MyFooCache(*args)

        # set value
        mycache.set(value)

        # clear the whole PREFIX namespace
        MyFooCache.flush()
        # initial part(s) of keys can be used for finer control over keys.
        MyFooCache.flush('EXTRA_PREFIX')

    Or you can override the __init__ method to define strict positional
    args with docstrings.

    .. code-block:: python

        class MyFooCache(Cache):
            PREFIX = 'FOO'

            def __init__(self, model_name, obj_key):
                super(MyFooCache, self).__init__(model_name, obj_key)

    """
    PREFIX = 'DFT'
    SERIALIZE = True
    DEFAULT = None



    def __init__(self, *args, **kwargs):
        self.serialize = kwargs.get('serialize', self.SERIALIZE)
        self.key = self._make_key(args)

    @classmethod
    def _make_key(cls, args):
        return "%s:%s" % (cls.PREFIX, ':'.join(args))

    def __unicode__(self):
        return 'Cache object for %s' % self.key

    def get(self, default=None):
        """
        return the cached value or default if it can't be found

        :param default: default value
        :return: cached value
        """
        d = cache.get(self.key)
        return ((json.loads(d.decode('utf-8')) if self.serialize else d)
                if d is not None
                else (default or self.DEFAULT))

    def set(self, val, lifetime=None):
        """
        set cache value

        :param val: any picklable object
        :param lifetime: exprition time in sec
        :return: val
        """
        cache.set(self.key,
                  (json.dumps(val) if self.serialize else val))
        # lifetime or settings.DEFAULT_CACHE_EXPIRE_TIME)
        return val

    def delete(self):
        """
        Deletes the object.

        Returns:
            Cache backend response.
        """
        return cache.delete(self.key)

    def incr(self, delta=1):
        """
        Increment the value of item.

        Args:
            delta: Incrementation amount.

        Returns:
            Cache backend response.
        """
        return cache.incr(self.key, delta)

    def decr(self, delta=1):
        """
        Reduce the value of item.

        Args:
            delta: Reduction amount.

        Returns:
            Cache backend response.
        """
        return cache.decr(self.key, delta)

    def add(self, val):
        """
        Add given value to item (list)

        Args:
            val: A JSON serializable object.

        Returns:
            Cache backend response.
        """
        return cache.lpush(self.key, json.dumps(val) if self.serialize else val)

    def get_all(self):
        """
        Get all list items.

        Returns:
            Cache backend response.
        """
        result = cache.lrange(self.key, 0, -1)
        return (json.loads(item.decode('utf-8')) for item in result if
                item) if self.serialize else result

    def remove_all(self):
        """
        Remove items of the list.

        Returns:
            Cache backend response.
        """
        return cache.ltrim(self.key, 0, -1)

    def remove_item(self, val):
        """
        Removes given from the list.

        Args:
            val: Item

        Returns:
            Cache backend response.
        """
        return cache.lrem(self.key, json.dumps(val))

    @classmethod
    def flush(cls, *args):
        """
        Removes all keys in this current namespace
        If called from class itself, clears all keys starting with cls.PREFIX
        if called with args, clears keys starting with given cls.PREFIX + args

        Args:
            *args: Arbitrary number of arguments.

        Returns:
            List of removed keys.
        """
        return _remove_keys([], [(cls._make_key(args) if args else cls.PREFIX) + '*'])



class ImageContentCache(Cache):
    """
    Cache object for the image searchs.

    Args:
        key: keyword
    """
    PREFIX = 'IMC'
    SERIALIZE = False

    def __init__(self, id):
        super(ImageContentCache, self).__init__(id)

class ImageSearchCache(Cache):
    """
    Cache object for the image searchs.

    Args:
        key: keyword
    """
    PREFIX = 'IMG'

    def __init__(self, keyword):
        super(ImageSearchCache, self).__init__(keyword)

class SettingsCache(Cache):
    """
    Cache object for the image searchs.

    Args:
        key: keyword
    """
    PREFIX = 'SETT'
    # SERIALIZE = False

    def __init__(self, name):
        super(SettingsCache, self).__init__(name)


class Session(Cache):
    """
    Cache object for user sessions.

    Args:
        sessid: user session id.
    """
    PREFIX = 'SES'
    DEFAULT = {}

    def get(self, key, default=None):
        return super(Session, self).get().get(key, default)

    def set(self, **kwargs):
        val = super(Session, self).get()
        val.update(kwargs)
        super(Session, self).set(val)

    def __init__(self, sessid):
        super(Session, self).__init__(sessid)

class ClearCache(Cache):
    """
    Empty cache object to flush all cache entries
    """
    PREFIX = ''


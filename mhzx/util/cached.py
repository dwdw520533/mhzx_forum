# -*- encoding=utf-8 -*-
"""
Provide cache access mechanism.
"""
import re
import sys
import pickle
import random
import functools

KEY_CHARS = r'[^a-zA-Z0-9_-]'


def to_cache_key(cache_key):
    """
    Filter off non-supported characters for memcached key
    string.
    """
    if type(cache_key) is not str:
        cache_key = cache_key.encode('utf-8', 'ignore')
    return re.sub(KEY_CHARS, '', cache_key)


class Cached(object):
    """
    A decorator to wrap the return value of function
    in the cache.

    parameters for init
    -------------------
    clients: list of cache clients,
        The clients used for cache access.

    parameters
    ----------
    key: string or callable,
        The cache key, if it is callable, the parameters
        is of the form "*sub, **kw", which is the parameters
        of the wrapped function.
    timeout: integer,
        How long the key is to be timeout in cache.
    log_to: function, default None,
        Accept function like log(msg), if provided, hit/miss
        log will be logged via the function.

    parameters when calling
    -----------------------
    __force_refill: boolean,
        Default False, whether to refill the cache.

    example
    -------
    cached = Cached(clients)

    @cached(key=lambda *sub, **kw: 'user_%s' % kw['user_id'],
            timeout=60):
    def user_profile(user_id=None):
        # Get user profile info
        return profile
    """

    def __init__(self, *clients, **kwargs):
        self._clients = clients
        self.persistence_cache_switch = kwargs.get('persistence_cache', False)
        self.persistence_cache_get = None
        self.persistence_cache_save = None
        self.send_mail = None

    def _fill(self, depth, key, value, timeout):
        timeout_factor = len(self._clients) - depth
        for client in self._clients[depth::-1]:
            reduced_timeout = timeout / timeout_factor \
                if timeout else timeout
            timeout_factor += 1
            client.set(key, value, reduced_timeout)

    def _get(self, key, timeout, func, __force_refill, log_to, p_cache, *sub, **kw):
        if __force_refill:
            ret = None
        else:
            for i, client in enumerate(self._clients):
                ret = client.get(key)
                if ret is not None:
                    if i > 0:
                        self._fill(i - 1, key, ret, timeout)
                    break
        if ret is None:
            log_to("Key %s miss." % key)

            try:
                ret = func(*sub, **kw)
            except Exception as e:
                if p_cache and callable(self.persistence_cache_get) and callable(self.persistence_cache_save):

                    if self.send_mail and callable(self.send_mail):
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        self.send_mail(exc_type, exc_value, exc_traceback)

                    value = self.persistence_cache_get(key)
                    if value:

                        log_to("key %s hit in persistence_cache." % key)

                        ret = pickle.loads(value)
                        self._fill(len(self._clients) - 1, key, ret, timeout)
                    else:
                        log_to("key %s missed in persistence_cache." % key)
                        raise e
                else:
                    raise e
            else:
                self._fill(len(self._clients) - 1, key, ret, timeout)

                if p_cache and (random.random() < 0.1 or __force_refill):
                    self.persistence_cache_save(key, pickle.dumps(ret), log_to=log_to)
        else:
            log_to("Key %s hit." % key)
        return ret

    def __call__(self, key, timeout, log_to=None, persistence_cache=None):
        log_to = log_to if log_to else lambda x: None

        def entangle(func):
            @functools.wraps(func)
            def wrapper(*sub, **kwargs):
                __force_refill = kwargs.pop('__force_refill', False)
                __log_to = kwargs.pop('__log_to', None) or log_to
                cache_key = key(*sub, **kwargs) if callable(key) else key
                cache_key = to_cache_key(cache_key)
                cache_timeout = timeout(*sub, **kwargs) if callable(timeout) else timeout
                p_cache = persistence_cache if isinstance(persistence_cache, bool) else self.persistence_cache_switch
                ret = self._get(cache_key, cache_timeout,
                                func, __force_refill, __log_to, p_cache,
                                *sub, **kwargs)
                return ret

            return wrapper

        return entangle

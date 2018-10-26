import time
import datetime
import logging
import threading
import six

logger = logging.getLogger("cache_lock")


def lock_maker(client=None, timeout=5):
    '''
    Factory method for generating a lock class,
    based on the given memcache client.

    The lock uses a cache client which supporting
    atomic add operation.

    Parameters
    ----------
    key: string
        The identifier of the lock, only the
        code blocks with the same key may race
        for the lock.
    timeout: integer, default 5
        The timeout of the lock, if the code could
        not hold the lock within the threshold,
        the code will be executed anyway.
    Example
    -------
    cache_lock = lock_maker(cache)
    with cache_lock('user10489'):
        # ...
        # the code block in the with statement
        # will be locked with key 'user10489'.
    '''
    cls = type("CacheLock", (object,), {})

    def __init__(self, key, timeout=5):
        self.key = 'lock_%s' % str(key)
        self.timeout = timeout

    def __enter__(self):
        while not client.add(self.key, 1, self.timeout):
            time.sleep(0.01)
        logger.debug("[ENTER]\t%s\t%s\t%s" % (self.key,
                                             id(threading.current_thread()),
                                             datetime.datetime.now()))

    def __exit__(self, exc_type, exc_value, traceback):
        client.delete(self.key)
        logger.debug("[ EXIT]\t%s\t%s\t%s" % (self.key,
                                             id(threading.current_thread()),
                                             datetime.datetime.now()))
        if exc_type is not None:
            six.reraise(exc_type, exc_value, traceback)

    cls.__init__ = __init__
    cls.__enter__ = __enter__
    cls.__exit__ = __exit__

    return cls

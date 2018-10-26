from mhzx.util.tinycache import TinyCache
from mhzx.util.cached import Cached
from mhzx.util.lock import lock_maker


cache = TinyCache(1000)
cached = Cached(cache)
cache_lock = lock_maker(cache)

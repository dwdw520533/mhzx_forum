'''
TinyCache
---------
A in process lru cache, support timeout of keys.

Usage Example:
Create a in process cache with capacity 20.

    cache = TinyCache(20)

Set an element, with timeout of 30 secs:

    cache.set('name', 'content', 30)

Get an element:

    cache.get('name')

Add an element, with timeout of 60 secs:

    cache.add('name', 'content2', 60)
    # If there is already a valid item with key 'name',
    # the add operation will return a False.

Delete an element:

    cache.delete('name')

Clear all keys fromt the document:

    cache.clear()

Multi get, get a list of keys:

    cache.get_multi(['key1', 'key2'])

Dump current objects in cache:

    cache.dump()
'''
from __future__ import with_statement
import sys
import time
import copy
import threading
import functools


def locked(func):
    @functools.wraps(func)
    def wrapper(self, *p, **kw):
        with self._lock:
            return func(self, *p, **kw)
    return wrapper


def stat(func):
    @functools.wraps(func)
    def wrapper(self, *p, **kw):
        ret = func(self, *p, **kw)
        if self._enable_stats:
            self._stats['%s_cnt' % func.__name__] += 1
            if ret and func.__name__ != 'set':
                self._stats['%s_hit' % func.__name__] += 1
        return ret
    return wrapper


class CacheNode:
    def __init__(self, key, value, timeout=0, prev=None, next=None):
        self.key = key
        self.value = value
        self.timeout = timeout
        self.prev = prev
        self.next = next

    def expired(self):
        return (self.timeout and self.timeout < time.time())

    def __repr__(self):
        return "<Node %s, key=%s, prev=%s, next=%s, expired=%s>"\
               % (hex(id(self)),
                  repr(self.key),
                  repr(self.prev.key if self.prev else None),
                  repr(self.next.key if self.next else None),
                  self.expired())


class TinyCache(object):
    def __init__(self, capacity, enable_stats=False):
        '''
        capacity is max number of item.
        '''
        if capacity <= 0:
            raise Exception("capacity should be a positive inteter.")
        self._data = {}
        self._capacity = capacity
        self._lock = threading.Lock()
        self._head = None
        self._tail = None
        self._stats = {'add_cnt': 0,
                       'add_hit': 0,
                       'get_cnt': 0,
                       'get_hit': 0,
                       'set_cnt': 0,
                       'delete_cnt': 0,
                       'delete_hit': 0}
        self._enable_stats = enable_stats

    def _pop_node(self, node):
        '''
        Pop a node from the priority linked list.
        '''
        if node.prev:
            node.prev.next = node.next
        else:
            self._head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self._tail = node.prev

    def _insert_node(self, node):
        '''
        Insert a node to front of the priority linked list.
        '''
        node.next = self._head
        node.prev = None
        if self._head:
            self._head.prev = node
        if not self._tail:
            self._tail = node
        self._head = node

    def _lru(self, node):
        '''
        Move to node to front.
        '''
        self._pop_node(node)
        self._insert_node(node)

    def _new_node(self, key, value, timeout):
        node = CacheNode(key, value, timeout=timeout)
        self._insert_node(node)
        return node

    def _check_and_truncate(self):
        '''
        Check if the current cache size, remove the
        nodes from tail if the size is over the capacity.
        '''
        if len(self._data) > self._capacity:
            node = self._tail
            self._pop_node(node)
            if node.key in self._data:
                del self._data[node.key]

    def _del_data(self, node):
        '''
        Set the node's reference to other node to None,
        and delete the node from self._data.
        '''
        node.prev = node.next = node.value = None
        del self._data[node.key]

    @stat
    @locked
    def set(self, key, value, timeout=0):
        '''
        Set cache key with value.
        The timeout value is in seconds.
        '''
        if timeout:
            timeout = timeout + time.time()
        node = self._data.get(key)
        if node is None:
            node = self._new_node(key, copy.copy(value), timeout)
        else:
            self._lru(node)
            node.value = copy.copy(value)
            node.timeout = timeout
        self._data[key] = node
        self._check_and_truncate()

    @stat
    @locked
    def get(self, key):
        '''
        Get the value of the key.
        '''
        node = self._data.get(key)
        if node is None:
            return None
        elif node.expired():
            self._pop_node(node)
            del self._data[key]
            return None
        else:
            self._lru(node)
            return copy.copy(node.value)

    def get_multi(self, keys, key_prefix=''):
        ret = {}
        for key in keys:
            value = self.get("%s%s" % (key_prefix, key))
            if value is not None:
                ret[key] = value
        return ret

    @stat
    @locked
    def delete(self, key):
        '''
        Delete the key.
        '''
        node = self._data.get(key)
        if node is None:
            return False
        elif node.expired():
            self._pop_node(node)
            self._del_data(node)
            return False
        else:
            self._pop_node(node)
            self._del_data(node)
            return True

    @stat
    @locked
    def add(self, key, value, timeout=0):
        '''
        Add the key, return True if success, False if
        the key exists.
        '''
        if timeout:
            timeout = timeout + time.time()
        node = self._data.get(key)
        if node is None:
            node = self._new_node(key, copy.copy(value), timeout)
            self._data[key] = node
            self._check_and_truncate()
            return True
        elif node.expired():
            self._lru(node)
            node.value, node.timeout = copy.copy(value), timeout
            return True
        else:
            return False


    @stat
    @locked
    def incr(self, key, delta=1):
        node = self._data.get(key)
        if node and not node.expired():
            node.value = node.value + delta
            self._lru(node)
            return node.value


    @stat
    @locked
    def decr(self, key, delta=1):
        node = self._data.get(key)
        if node and not node.expired():
            node.value = node.value - delta
            self._lru(node)
            return node.value


    def dump(self):
        '''
        Dump all keys alone with prev/next for debugging.
        '''
        curr = self._head
        sys.stdout.write("Head: %s" % self._head)
        while curr is not None:
            sys.stdout(curr)
            curr = curr.next
        sys.stdout.write("Tail: %s" % self._tail)

    def get_stats(self):
        ret = self._stats
        ret['item_cnt'] = len(self._data)
        return ret

    def print_stats(self):
        ret = ''
        for k, v in sorted(self.get_stats().items(),
                           key=lambda x: x[0]):
            ret += '%s:\t%s\n' % (k, v)
        sys.stdout.write(ret)

    @locked
    def clear(self):
        '''
        Clear the all the keys in cache.
        '''
        nodes = self._data.values()
        for node in nodes:
            self._del_data(node)
        self._head = self._tail = None

class LRUCache:
    def __init__(self, capacity=10):
        self.hash_map = {}
        self.caches_ordered = []
        self.capacity = capacity

    def get(self, key):
        if key in self.hash_map:
            return self.hash_map[key]
        else:
            return ''

    def set(self, key, value):
        if key in self.hash_map:
            self.hash_map[key] = value

        else:
            if len(self.caches_ordered) == self.capacity:
                to_delete_key = ''
                for k, v in self.hash_map.items():
                    if v == self.caches_ordered[0]:
                        to_delete_key = k
                        break
                self.delete(to_delete_key)

        self.caches_ordered.append(value)
        self.hash_map[key] = value

    def delete(self, key):
        if key in self.hash_map:
            self.caches_ordered.remove(self.hash_map[key])
            del self.hash_map[key]


if __name__ == "__main__":
    cache = LRUCache(100)
    cache.set('Jesse', 'Pinkman')
    cache.set('Walter', 'White')
    cache.set('Jesse', 'James')
    print(cache.get('Jesse'))
    cache.delete('Walter')
    print(cache.get('Walter'))
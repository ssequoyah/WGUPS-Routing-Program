# Create Hash Map class

class HashMap:
    def __init__(self, initial_capacity=20):
        self.table = []
        for _ in range(initial_capacity):
            self.table.append([])

    def insert(self, key, item):
        bucket = self.table[hash(key) % len(self.table)]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, item)
                return True
        bucket.append((key, item))
        return True

    def lookup(self, key):
        bucket = self.table[hash(key) % len(self.table)]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def remove(self, key):
        bucket = self.table[hash(key) % len(self.table)]
        for pair in bucket:
            k, v = pair
            if k == key:
                bucket.remove(pair)
                return True
        return False

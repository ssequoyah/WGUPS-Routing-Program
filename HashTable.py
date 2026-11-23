
# initialize hashmap class
class HashMap:
    def __init__(self, initial_capacity=50):
        self.list = []
        for i in range(initial_capacity):
            self.list.append([])
        # Inserts a new item into the hash table
        # Citing source: WGU code repository W-2_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy.py

    # inserts into and updates hash table
    def insert(self, key, item):
        # find the item destination bucket
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        # update key if it's already in bucket
        for kv in bucket_list:  # O(N) CPU time
            # print the key value
            if kv[0] == key:
                kv[1] = item
                return True

        # if not, insert the item on the end of bucket list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Find items in hash table

    def lookup(self, key):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]
        for pair in bucket_list:
            if key == pair[0]:
                return pair[1]
        # pair[0] will never match key[0]
        return None


    # Removes item from hash table

    def hash_remove(self, key):
        slot = hash(key) % len(self.list)
        destination = self.list[slot]

        # If key is found, remove item
        if key in destination:
            destination.remove(key)
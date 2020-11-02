class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return  (f"HashtableEntry("
                f"\n\tkey={self.key}"
                f"\n\tvalue={self.value}\n")


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):
        if capacity < MIN_CAPACITY:
            self.capacity = MIN_CAPACITY
        else:
            self.capacity = capacity
        self.storage = [None] * capacity
        self.old_storage = None
        self.count = 0


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return len(self.storage)


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        return self.count / self.get_num_slots()


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """

        FNV_offset_basis = 14695981039346656037
        FNV_prime = 1099511628211

        for x in key:
            FNV_offset_basis = FNV_offset_basis * FNV_prime
            FNV_offset_basis = FNV_offset_basis ^ ord(x)
        return FNV_offset_basis


    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        DJB2_HASH = 5381

        for x in key:
            DJB2_HASH = ((DJB2_HASH << 5) + DJB2_HASH) + ord(x)
        return DJB2_HASH


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        # return self.fnv1(key) % self.capacity
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        i = self.hash_index(key)
        
        if self.storage[i] is None:
            self.storage[i] = HashTableEntry(key, value)
        else:
            new_entry = HashTableEntry(key, value)
            new_entry.next = self.storage[i]
            self.storage[i] = new_entry
        self.count += 1
        return None


    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        i = self.hash_index(key)
        temp = self.storage[i]

        while temp.next is not None:
            if temp.key == key:
                temp.value = None
                return None
            else:
                temp = temp.next
        if temp.next is None:
            if temp.key == key:
                temp.value = None
        self.count -= 1
        return None



    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        i = self.hash_index(key)
        temp = self.storage[i]

        while temp:
            if temp.key == key:
                return temp.value
            temp = temp.next
        return None

    def should_resize(self):
        load_factor = self.get_load_factor()
        num_slots = self.get_num_slots()
        if load_factor > 0.7:
            self.resize(int(num_slots * 2))
        if load_factor < 0.2:
            self.resize(int(num_slots / 2))
        return None

    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """

        if new_capacity < MIN_CAPACITY:
            return None
        else:
            self.old_storage = self.storage
            self.storage = [None] * new_capacity
            self.capacity = new_capacity
            self.count = 0
        
        for slot in self.old_storage:
            temp = None
            if slot is not None:
                self.put(slot.key, slot.value)
            if next in self.__dict__:
                temp = slot.next
            while temp is not None:
                self.put(temp.key, temp.value)
                temp = temp.next

        self.old_storage = None
        return None
        



if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")

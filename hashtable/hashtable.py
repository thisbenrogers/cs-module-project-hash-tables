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
        return  (f"HashTableEntry("
                f"\n\tkey={self.key}"
                f"\n\tvalue={self.value}\n)")

    def get_value(self):
        return self.value
    def get_next(self):
        return self.next
    def set_next(self, new_next):
        self.next = new_next

# Linked List to manage chaining collisions
class LinkedList:
    def __init__(self):
        self.head = None
        self.length = 0

    def __str__(self):
        return f"length: {self.length}"

    def __repr__(self):
        return  (f"LinkedList("
                f"\n\thead={self.head}"
                f"\n\tlength={self.length}\n)")

    def find(self, key):
        current_entry = self.head
        while current_entry is not None:
            if key == current_entry.key:
                return current_entry.value
            else: 
                current_entry == current_entry.next
        return None

    
    def add_to_head(self, key, value):
        new_entry = HashTableEntry(key, value, self.head)
        self.head = new_entry
        self.length += 1

    def delete_entry(self, key):
        temp = self.head
        if temp is not None and temp.key == key:
            self.head = temp.next
            temp = None
            return
        while temp is not None:
            if temp.key == key:
                break
            prev = temp
            temp = temp.next
        if temp == None:
            print('Not Found')
            return
        prev.next = temp.next
        temp = None
        self.length -= 1


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
        DJB2_hash = 5381

        for x in key:
            DJB2_hash = ((DJB2_hash << 5) + DJB2_hash) + ord(x)
        return DJB2_hash & 0xFFFFFFFF

    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        # return self.fnv1(key) % self.get_num_slots()
        return self.djb2(key) % self.get_num_slots()

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        i = self.hash_index(key)
        if self.storage[i] is None:
            new_list = LinkedList()
            new_list.add_to_head(key, value)
            self.storage.insert(i, new_list)
        else:
            old_list = self.storage[i]
            old_list.add_to_head(key, value)
            print(f"old_list: {old_list} -- head: {old_list.head} -- next: {old_list.head.next}")
        self.count += 1

        ### Test for resizing
        # if (self.get_load_factor() > 0.7):
            # Double size of Array
            # Then copy everything over, one at a time, re-hashing again

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        i = self.hash_index(key)
        linked_list = self.storage[i]
        linked_list.delete_entry(key)
        self.count -= 1

        ### Test for resizing
        # if (self.get_load_factor() < 0.2):
            # THIS IS A STRETCH GOAL
            # Cut the Array down in half
            # Then copy everything over, one at a time, re-hashing again

    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        i = self.hash_index(key)
        print(f"i {i}")
        if self.storage[i] is None:
            return None
        linked_list = self.storage[i]
        text = linked_list.find(key)
        if text is None:
            return None
        return text
        
    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        pass


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

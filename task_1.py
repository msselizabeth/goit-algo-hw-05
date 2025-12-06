class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        key_hash = self.hash_function(key)
        key_value = [key, value]

        if self.table[key_hash] is None:
            self.table[key_hash] = list([key_value])
            return True
        else:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.table[key_hash].append(key_value)
            return True

    def get(self, key):
        key_hash = self.hash_function(key)
        if self.table[key_hash] is not None:
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None
    
    def delete(self, key):
        key_hash = self.hash_function(key)
        key_value = self.table[key_hash]
        
        if key_value is not None:
            for i, pair in enumerate(key_value):
                if pair[0] == key:
                    del key_value[i]
                    return True
        return False
    
    def visualize(self):
        print(f"{'\nIndex':<8} | {'Bucket Contents'}")
        print("-" * 35)
        
        for i, value in enumerate(self.table):
            if value:
                print(f"{i:<7} | {value}")
            else:
                print(f"{i:<7} | [ ]")
        print("-" * 35)
        


H = HashTable(5)
H.insert("apple", 10)
H.insert("orange", 20)
H.insert("banana", 30)

print(H.get("apple"))   
print(H.get("orange"))  
print(H.get("banana"))  

# Print the table
H.visualize()

# delete by key
res = H.delete("apple")
print(f"\nDeleted? — {res}")

H.visualize()

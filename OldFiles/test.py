import hashlib
import time

def get_md5_of_string(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()

# Measure the time to hash 1000 strings
start_time = time.time()

hashlist = []
for i in range(10000000):
    hashlist.append(get_md5_of_string(f"test{i}")[:10])

end_time = time.time()
print(f"Time taken to hash x strings: {end_time - start_time} seconds")

# Checking how many hash collisions there are
unique_hashes = set(hashlist)
print(f"Number of unique hashes: {len(unique_hashes)}")
print(f"Number of total hashes: {len(hashlist)}")
print(f"Number of hash collisions: {len(hashlist) - len(unique_hashes)}")
print(f"Percentage of hash collisions: {(len(hashlist) - len(unique_hashes)) / len(hashlist) * 100}%")




# Measure the time to search for a hash in the list of hashes x times + worst case
target_hash = hashlist[-1]

start_time = time.time()

for i in range(100):
    target_hash in hashlist

end_time = time.time()


print(f"Time taken to search for a hash in the list of hashes x times: {end_time - start_time} seconds")
print(f"Time taken to search for a hash in the list of hashes 1 time: {(end_time - start_time) / 100} seconds")
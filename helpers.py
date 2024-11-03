# Imports
import hashlib
from bloomfilter import BloomFilter
import os




# Clamp a number between a range
def clamp(n, min_value, max_value):
    return max(min_value, min(n, max_value))


# Hashing URL
def getHash(inputString, numChars=10):
    return hashlib.md5(inputString.encode()).hexdigest()[:numChars]


# Saving and loading the bloom filter
def saveBF(bf : BloomFilter, path):
    dump = bf.dumps_to_hex()

    # Delete the existing file if it exists
    if os.path.exists(path):
        os.remove(path)

    with open(path, 'w') as f:
        f.write(dump)

def loadBF(path):
    with open(path, 'r') as f:
        dump = f.read()

    bf = BloomFilter.loads_from_hex(dump)
    return bf

# testing how big bf's get depending on the number of expected inserts and false positive rate
from bloomfilter import BloomFilter

expectedInserts = 1000000000
falsePosRate = 0.01
bf = BloomFilter(expectedInserts, falsePosRate)

print(f"Expected inserts: {expectedInserts}")
print(f"False positive rate: {falsePosRate}")
print(f"Size of the bloom filter: {bf.num_of_bits(expectedInserts, falsePosRate)} bits")
print(f"Number of hash functions: {bf.num_of_hash_functions(expectedInserts, bf.num_of_bits(expectedInserts, falsePosRate))}")
print('---------------------------------')
print(f"Size of the bloom filter: {bf.num_of_bits(expectedInserts, falsePosRate)/8} bytes")
print(f"Size of the bloom filter: {bf.num_of_bits(expectedInserts, falsePosRate)/8/1024} kilobytes")
print(f"Size of the bloom filter: {bf.num_of_bits(expectedInserts, falsePosRate)/8/1024/1024} megabytes")
print(f"Size of the bloom filter: {bf.num_of_bits(expectedInserts, falsePosRate)/8/1024/1024/1024} gigabytes")
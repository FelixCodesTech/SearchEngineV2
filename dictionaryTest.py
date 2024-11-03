# This is just a test of how different dictionary sizes affect lookup times

# Imports
import time
import random
import sys

# Functions
def createDict(size: int):
    d = {}
    for i in range(size):
        d[i] = f'{pow(i, 2)} is the square of {i}'
    return d

def lookupDict(d: dict, size: int):
    totalTime = 0
    startTime = time.time()
    for _ in range(5):
        key = random.randint(0, size-1)
        val = d[key]
        # print(f"Key: {key}    Value: {val}")

    endTime = time.time()
    totalTime = endTime - startTime
    timePerLookup = totalTime / 5

    formattedTime = f"{totalTime:.6f}"

    return formattedTime

# Main
startSize = 1
endSize = 10000010
step = 1000000

for size in range(startSize, endSize, step):
    d = createDict(size)
    timeTaken = lookupDict(d, size)
    memoryUsage = sys.getsizeof(d)
    print(f"Size: {size}        Time taken: {timeTaken}        Memory usage: {memoryUsage} bytes")
    print(f'Memory usage: {memoryUsage} bytes ({memoryUsage/1024/1024} MB)')
    print(f'-'*30)
    
    time.sleep(5)

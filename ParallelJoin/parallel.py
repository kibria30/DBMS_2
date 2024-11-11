import random
import time
from concurrent.futures import ProcessPoolExecutor

size = 10000
random.seed(42)
table_1 = [0] * size
table_2 = [0] * size

for i in range(size):
    table_1[i] = random.randint(1, size * 2)
    table_2[i] = i + 1

table_11 = table_1[:size // 4]
table_12 = table_1[size // 4:size // 2]
table_13 = table_1[size // 2: size - (size // 4)]
table_14 = table_1[size - (size // 4):]

def parallel_function(target, given):
    joined_list = []
    for i in target:
        for j in given:
            if i == j:
                joined_list.append(i)
    return joined_list

# single processor
print("Single processor:")
start = time.time()
result = parallel_function(table_2, table_1)

end = time.time()

print("Total joined elements:", len(result))
print("Time taken for single processor:", end - start, "seconds")


# 4 processor
print("\n4 processors:")
start = time.time()

with ProcessPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(parallel_function, [table_2] * 4, [table_11, table_12, table_13, table_14]))

end = time.time()

joined = [item for sublist in results for item in sublist]
print("Total joined elements:", len(joined))
print("Time taken by 4 processor::", end - start, "seconds")
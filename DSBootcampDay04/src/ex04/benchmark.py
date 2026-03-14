import timeit
import random
from collections import Counter

def my_function(numbers):
    new_dict = dict()
    for item in numbers:
        new_dict[item] = new_dict.get(item, 0) + 1
    return new_dict

def my_tops(numbers):
    new_dict = my_function(numbers)
    sorted_dict = sorted(new_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_dict[:10]

def counters_top(numbers):
    new_dict = Counter(numbers)
    return new_dict.most_common(10)

if __name__ == "__main__":
    numbers = [random.randint(1, 100) for _ in range(1000000)]
    print(f"my function: {timeit.timeit(lambda: my_function(numbers), number=1)}")
    print(f"Counter: {timeit.timeit(lambda: Counter(numbers), number=1)}")
    print(f"my top: {timeit.timeit(lambda: my_tops(numbers), number=1)}")
    print(f"Counter's top: {timeit.timeit(lambda: counters_top(numbers), number=1)}")
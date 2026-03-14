import timeit
import sys
from functools import reduce

def loop_counting(numbers):
    sum = 0
    for x in numbers:
        sum = sum + x * x
    return sum

def add(x,y):
    return x + y

def reduce_counting(numbers):
    return reduce(add,numbers)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python benchmark.py <function_name> <number_of_iterations>")
        sys.exit(1)
    name = sys.argv[1]
    try:
        iterations = int(sys.argv[2])
        number = int(sys.argv[3])
    except ValueError:
        print("Both iterations and number must be integers.")
        sys.exit(1)
    numbers = list(range(1, number + 1))
    if name == "loop":
        print(timeit.timeit("loop_counting(numbers)",globals=globals(),number=iterations))
    elif name == "reduce":
        print(timeit.timeit("reduce_counting(numbers)", globals=globals(), number=iterations))
    else:
        print(f"Function '{name}' is not recognized.\nIt should be either 'loop' or 'reduce'!")
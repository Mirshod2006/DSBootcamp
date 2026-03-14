import sys
import resource

def fetch_file(filename):
    try:
        with open(filename,"r") as file:
            for line in file:
                yield line
    except FileNotFoundError as e:
        print(f"Error: {e}")
        yield []


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ordinary.py <filename>")
        sys.exit(1)
    start_usage = resource.getrusage(resource.RUSAGE_SELF)
    filename = sys.argv[1]
    for line in fetch_file(filename):
        pass
    end_usage = resource.getrusage(resource.RUSAGE_SELF)
    user_time = end_usage.ru_utime - start_usage.ru_utime
    sys_time = end_usage.ru_stime - start_usage.ru_stime
    total_time = user_time + sys_time
    peak_memory = end_usage.ru_maxrss / (1024 ** 2)
    print(f"Peak Memory Usage = {peak_memory:.3f} GB")
    print(f"User Mode Time + System Mode Time = {total_time:.2f}s")

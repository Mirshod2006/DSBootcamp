import sys
import timeit

def loop(emails):
    new_emails = []
    for email in emails:
        new_emails.append(email)

def list_comprehension(emails):
    new_emails = [email for email in emails]

def list_map(emails):
    new_emails = list(map(lambda x: x, emails))

def list_filter(emails):
    new_emails = list(filter(lambda x: x, emails))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 benchmark.py <function_name> <number_of_iterations>")
        sys.exit()
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com',
              'james@gmail.com', 'john@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com',
              'anna@live.com', 'james@gmail.com', 'alice@yahoo.com', 'john@gmail.com', 'philipp@gmail.com',
              'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com',
              'philipp@gmail.com', 'john@gmail.com', 'james@gmail.com', 'anna@live.com','alice@yahoo.com']
    function_name = sys.argv[1]
    number_of_iterations = 0
    try:
        number_of_iterations = int(sys.argv[2])
    except ValueError:
        print("Please enter a valid number, Do Not enter a string nor a float!")
        sys.exit()
    if function_name == "loop":
        print(timeit.timeit("loop(emails)",globals=globals(),number=number_of_iterations))
    elif function_name == "list_comprehension":
        print(timeit.timeit("list_comprehension(emails)",globals=globals(),number=number_of_iterations))
    elif function_name == "map":
        print(timeit.timeit("list_map(emails)",globals=globals(),number=number_of_iterations))
    elif function_name == "filter":
        print(timeit.timeit("list_filter(emails)",globals=globals(),number=number_of_iterations))
    else:
        print("Invalid function name!")
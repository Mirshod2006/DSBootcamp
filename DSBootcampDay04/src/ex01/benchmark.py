import timeit

def usual_for(emails):
    new_list = []
    for email in emails:
        new_list.append(email)

def list_comprehension(emails):
    new_list = [x for x in emails]

def looping_with_map(emails):
    new_list = list(map(str, emails))

if __name__ == '__main__':
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com',
              'james@gmail.com', 'john@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com',
              'anna@live.com', 'james@gmail.com', 'alice@yahoo.com', 'john@gmail.com', 'philipp@gmail.com',
              'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com',
              'philipp@gmail.com', 'john@gmail.com', 'james@gmail.com', 'anna@live.com','alice@yahoo.com']
    time1 = timeit.timeit("list_comprehension(emails)", globals=globals(), number=90000000)
    time2 = timeit.timeit("usual_for(emails)", globals=globals(), number=90000000)
    time3 = timeit.timeit("looping_with_map(emails)", globals=globals(), number=90000000)
    if time1 <= time2:
        if time1 <= time3:
            print("it is  better to use a list comprehension")
            print(f'{time1} vs {time2} vs {time3}')
        else:
             print("it is better to use a map function")
             print(f'{time1} vs {time2} vs {time3}')
    else:
        if time2 <= time3:
            print("it is  better to use a loop")
            print(f'{time1} vs {time2}')
        else:
            print("it is better to use a map function")
            print(f'{time1} vs {time2} vs {time3}')
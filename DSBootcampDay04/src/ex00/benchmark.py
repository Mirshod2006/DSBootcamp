import timeit

def usual_for(emails):
    new_list = []
    for email in emails:
        new_list.append(email)

def list_comprehension(emails):
    new_list = [x for x in emails]

if __name__ == '__main__':
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com',
              'james@gmail.com', 'john@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com',
              'anna@live.com', 'james@gmail.com', 'alice@yahoo.com', 'john@gmail.com', 'philipp@gmail.com',
              'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com',
              'philipp@gmail.com', 'john@gmail.com', 'james@gmail.com', 'anna@live.com','alice@yahoo.com']
    
    # time1_str = timeit.default_timer()
    # for i in range(0,90000000):
    #     usual_for(emails)
    # time1_end = timeit.default_timer()
    # time1 = time1_end - time1_str
    # time2_str = timeit.default_timer()
    # for i in range(0,90000000):
    #     list_comprehension(emails)
    # time2_end = timeit.default_timer()
    # time2 = time2_end - time2_str
    time2 = timeit.timeit("usual_for(emails)", globals=globals(), number=90000000)
    time1 = timeit.timeit("list_comprehension(emails)", globals=globals(), number=90000000)
    if time1 <= time2:
        print("it is  better to use a list comprehension")
        print(f'{time1} vs {time2}')
    else:
        print("it is  better to use a loop")
        print(f'{time1} vs {time2}')
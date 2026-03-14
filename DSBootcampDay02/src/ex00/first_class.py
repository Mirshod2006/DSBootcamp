class Must_read():
    with open("data.csv",'r') as data:
        lines = data.readlines()
        count = 0
        for line in lines:
            count += 1
            char = '' if (count != len(lines)) else '\n'
            print(line, end=char)

if __name__ == '__main__':
    read = Must_read()
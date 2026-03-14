class Research():
    def __init__(self):
        pass
    def file_reader(self):
        with open("../ex00/data.csv",'r') as data:
            lines = data.readlines()
            text = ''
            for line in lines:
                text += line
            return text

if __name__ == '__main__':
    research = Research()
    print(research.file_reader())
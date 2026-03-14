import sys
from random import randint

class Calculations:
    def __init__(self,path):
        self.path = path
        self.data = self.file_reader()

    def counts(self):
            head, tail = 0, 0
            for numbers in self.data:
                if numbers[0] == 1:
                    head += 1
                if numbers[1] == 1:
                    tail += 1
            return [head,tail]

    def file_reader(self):
        has_header=True
        try:
            with open(self.path,"r") as data:
                lines = data.readlines()
                if has_header:
                    lines = lines[1:]
                result = []
                for line in lines:
                    clean_line = [1 if ch == '1' else 0 for ch in line.strip() if ch in "01"]
                    if clean_line:
                        result.append(clean_line)
                return result
                       

        except FileNotFoundError:
            print(f"{self.path}: No such file or directory!")
            return []

    def fractions(self):
            head ,tail = self.counts()
            total = head + tail
            if total == 0:
                return [0, 0]
            head_fraction = (head / total) * 100
            tail_fraction = (tail / total) * 100
            return [head_fraction, tail_fraction]

class Analytics(Calculations):
    def __init__(self, path, number):
        super().__init__(path)
        self.number = number
    
    def predict_random(self):
        return [[1,0] if randint(0,1) else [0,1] for _ in range(self.number)]


    def predict_last(self):
        return self.data[-1] if self.data else []
    
    def save_file(self, data, filename):
        with open(f"{filename}.txt","w") as file:
            file.write(data)
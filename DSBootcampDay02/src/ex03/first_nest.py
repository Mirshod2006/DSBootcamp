import os
import sys

class Research:
    def __init__(self, path):
        self.path = path
        data = self.file_read(has_header=True)
        print(data)
        calculations = self.Calculation()
        count_result = calculations.count(data)
        print(f"{count_result[0]} {count_result[1]}")
        fraction_result = calculations.fractions(count_result[0],count_result[1])
        print(f"{fraction_result[0]} {fraction_result[0]}")
    
    def file_read(self, has_header=True):
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
        
    class Calculation:
            @staticmethod
            def count(data):
                head = 0
                tail = 0
                for numbers in data:
                    if numbers[0] == 1:
                        head += 1
                    if numbers[1] == 1:
                        tail += 1
                return [head,tail]
            @staticmethod
            def fractions(head,tail):
                total = head + tail
                if total == 0:
                    return [0, 0]
                head_fraction = (head / total) * 100
                tail_fraction = (tail / total) * 100
                return [head_fraction, tail_fraction]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 first_constructor.py <filename>")
        exit(1)
    else:
        Research(sys.argv[1])
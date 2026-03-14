import os
import sys

class Research:
    def __init__(self, path):
        self.path = path
        print(self.file_read())
    
    def file_read(self):
        try:
            with open(self.path,"r") as data:
                return data.read()
        except:
            print(f"{self.path}: No such file or directory!")
            return ""

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 first_constructor.py <filename>")
        exit(1)
    else:
        research = Research(sys.argv[1])
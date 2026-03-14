import sys
def names_extractor(path):
    with open(path, "r") as email_file, open("employees.tsv","w") as result:
        result.write("Name\tSurname\tE-mail\n")

        for line in email_file:
            line = line.strip()
            if "@" not in line or "." not in line:
                continue
            parts = line.split("@")[0].split(".")
            name = parts[0].capitalize()
            surname = parts[1].capitalize()
            result.write(f"{name}\t{surname}\t{line}\n")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage : python3 names_extractor.py <file_path>")
        sys.exit(1)

    path = sys.argv[1]
    names_extractor(path)
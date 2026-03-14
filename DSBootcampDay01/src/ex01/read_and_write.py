def read_and_write():
    infile = open("ds.csv","r")
    outfile = open("ds.tsv","r+")
    outfile.truncate(0)
    outfile.close()
    outfile = open("ds.tsv","w")
    lines = infile.readlines()
    for line in lines:
        newline = ""
        inside = False
        for ch in line:
            if ch == '"':
                inside = not inside
            if ch == ',' and not inside:
                newline += '\t'
            else:
                newline += ch
        outfile.writelines(newline)
    infile.close()
    outfile.close()

if __name__ == '__main__':
    read_and_write()
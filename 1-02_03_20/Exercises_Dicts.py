import sys

print(sys.argv)
option = sys.argv[1]
file = "test.txt"#sys.argv[2]
    
def count(file):
    f = open(file, "rt")
    count = 0
    for line in f:
        line.split("")
        count += len(line)
    return count

def topcount(file):
    topcount = count(file)
    return topcount[:21]

if option == "--count":
    print(count(file))
else:
    print(topcount(file))


import sys
from parser_ import Parser

if len(sys.argv) != 2:
    print("Usage: " + str(sys.argv[0]) + " file_name")
else:
    try:
        f = open(sys.argv[1], "r")
        program = f.read()
        print(program)
        p = Parser()
        p.parse(program)
    except IOError:
        print("Couldn't read file: " + sys.argv[1])

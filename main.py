import sys
from parser_ import Parser
from pkb import PKB
from query.query_evaluator import QueryEvaluator

if len(sys.argv) != 2:
    print("Usage: " + str(sys.argv[0]) + " file_name")
else:
    try:
        f = open(sys.argv[1], "r")
        program = f.read()
        print(program)
        p = Parser()
        ast = p.parse(program)

        pkb = PKB(ast)

        query_evaluator = QueryEvaluator(pkb)
        query_evaluator.load()

    except IOError:
        print("Couldn't read file: " + sys.argv[1])

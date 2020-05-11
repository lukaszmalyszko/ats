import sys
from parser_ import Parser
from pkb import PKB
from query.query_evaluator import QueryEvaluator


def load_file_to_pkb(file):
    program = file.read()
    ast = Parser().parse(program)
    return PKB(ast)


if len(sys.argv) != 2:
    print("Usage: " + str(sys.argv[0]) + " file_name")
else:
    try:
        f = open(sys.argv[1], "r")
        pkb = load_file_to_pkb(f)
        query_evaluator = QueryEvaluator(pkb)
        print("Ready")
        while True:
            query_evaluator.load()
            query_evaluator.get_result()
    except IOError:
        print("Couldn't read file: " + sys.argv[1])




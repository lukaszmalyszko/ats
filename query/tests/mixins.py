from unittest import TestCase

from parser_ import Parser
from pkb import PKB


class PkbTestCase(TestCase):
    def setUp(self) -> None:
        self.pkb = self.__load_simple_program()

    def __load_simple_program(self):
        f = open("test_data/bigger_program.txt", "r")
        program = f.read()
        f.close()
        p = Parser()
        ast = p.parse(program)
        return PKB(ast)

from unittest import TestCase
from unittest.mock import patch

from parser_ import Parser
from pkb import PKB
from query.query_evaluator import QueryEvaluator


class TestQueryEvaluator(TestCase):
    def setUp(self) -> None:
        self.expected_result = [
            "1, 3, 6, 8, 10, 12, 16, 17, 19, 20, 22, 23, 25, 29, 32, 34, 35, 36, 37",
            "3, 16, 19, 32, 37"
        ]
        self.pkb = self.__load_simple_program()
        self.query_evaluator = QueryEvaluator(self.pkb)

    def __load_simple_program(self):
        f = open("test_data/bigger_program.txt", "r")
        program = f.read()
        p = Parser()
        ast = p.parse(program)
        return PKB(ast)

    def test_select_statement_that_modifies_x(self):
        # Arrange
        variables = "stmt s;"
        query = "Select s such that Modifies(s,'x')"
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertIn(result, self.expected_result)

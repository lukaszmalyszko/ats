from unittest import TestCase
from unittest.mock import patch

from query.query_preprocessor import QueryPreprocessor


class TestQueryPreprocessor(TestCase):
    def setUp(self) -> None:
        self.query_preprocessor = QueryPreprocessor()
        self.variables = "stmt s, s1; assign a, a1, a2; while w; variable v; constant c; prog_line n, n1, n2;"
        self.query = "Select s such that Modifies(s,'x')"

    def test_creates_select_node(self):
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            self.query_preprocessor.get_input()
            select = self.query_preprocessor.tree.select
            self.assertTrue(select)
            self.assertEqual(select.variables[0].name, "s")

    def test_creates_modifies_node(self):
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            self.query_preprocessor.get_input()
            such_that = self.query_preprocessor.tree.get_such_that_statements()
            self.assertEqual(len(such_that), 1)

    def test_creates_with_node(self):
        self.query = "Select s such that Modifies(s, 'x') with s.stmt# = 10"
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            self.query_preprocessor.get_input()
            with_stmts = self.query_preprocessor.tree.get_with_statements()
            self.assertEqual(len(with_stmts), 1)

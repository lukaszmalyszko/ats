from unittest import TestCase
from unittest.mock import patch

from query.query_preprocessor import QueryPreprocessor


class TestQueryPreprocessor(TestCase):
    def setUp(self) -> None:
        self.query_preprocessor = QueryPreprocessor()
        self.variables = "stmt s, s1; assign a, a1, a2; while w; variable v; constant c; prog_line n, n1, n2;"
        self.query = "Select s such that Modifies(s,'x')"

    def test_creates_tree_root(self):
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            self.query_preprocessor.get_input()
            self.assertTrue(self.query_preprocessor.tree.root)

    def test_creates_select_node(self):
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            self.query_preprocessor.get_input()
            select = self.query_preprocessor.tree.root.select
            self.assertTrue(select)
            self.assertEqual(select.variables[0].name, "s")

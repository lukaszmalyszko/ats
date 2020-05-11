from unittest import TestCase
from unittest.mock import patch

from query.query_preprocessor import QueryPreprocessor
from query.tests.mixins import PkbTestCase


class TestQueryPreprocessor(PkbTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.query_preprocessor = QueryPreprocessor(self.pkb)
        self.variables = "stmt s, s1; assign a, a1, a2; while w; variable v; constant c; prog_line n, n1, n2;"
        self.query = "Select s such that Modifies(s,'x')"

    def test_creates_select_and_empty_result(self):
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            self.query_preprocessor.get_input()
            select = self.query_preprocessor.tree.select
            result = self.query_preprocessor.tree.result
            self.assertTrue(select)
            self.assertFalse(result)
            self.assertEqual(select.variables[0].name, "s")

    def test_creates_modifies_node(self):
        self.__then_query_tree_contains_such_that_node_with_string("s", "x")

    def test_creates_uses_node(self):
        self.query = "Select s such that Uses(s, 'x') with s.stmt# = 10"
        self.__then_query_tree_contains_such_that_node_with_string("s", "x")

    def test_creates_parent_node(self):
        self.query = "Select s such that Parent(s, s1) with s.stmt# = 10"
        self.__then_query_tree_contains_such_that_node("s", "s1")

    def test_creates_parent_star_node(self):
        self.query = "Select s such that Parent*(s, s1) with s.stmt# = 10"
        self.__then_query_tree_contains_such_that_node("s", "s1")

    def test_creates_follows_node(self):
        self.query = "Select s such that Follows(s, s1) with s.stmt# = 10"
        self.__then_query_tree_contains_such_that_node("s", "s1")

    def test_creates_follows_star_node(self):
        self.query = "Select s such that Follows*(s, s1) with s.stmt# = 10"
        self.__then_query_tree_contains_such_that_node("s", "s1")

    def test_creates_with_node(self):
        self.query = "Select s such that Modifies(s, 'x') with s.stmt# = 10"
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            self.query_preprocessor.get_input()
            with_stmts = self.query_preprocessor.tree.get_with_statements()
            self.assertEqual(len(with_stmts), 1)
            self.assertEqual(with_stmts[0].first_arg.name, "s")
            self.assertEqual(with_stmts[0].attr_name, "stmt#")
            self.assertEqual(with_stmts[0].second_arg, 10)

    def __then_query_tree_contains_such_that_node(self, first_arg, second_arg):
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            self.query_preprocessor.get_input()
            such_that = self.query_preprocessor.tree.get_such_that_statements()
            self.assertEqual(len(such_that), 1)
            self.assertEqual(such_that[0].first_arg.name, first_arg)
            self.assertEqual(such_that[0].second_arg.name, second_arg)

    def __then_query_tree_contains_such_that_node_with_string(
        self, first_arg, second_arg
    ):
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            self.query_preprocessor.get_input()
            such_that = self.query_preprocessor.tree.get_such_that_statements()
            self.assertEqual(len(such_that), 1)
            self.assertEqual(such_that[0].first_arg.name, first_arg)
            self.assertEqual(such_that[0].second_arg, second_arg)

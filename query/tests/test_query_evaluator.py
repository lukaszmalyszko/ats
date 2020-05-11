from unittest import TestCase
from unittest.mock import patch

from parser_ import Parser
from pkb import PKB
from query.query_evaluator import QueryEvaluator
from query.tests.mixins import PkbTestCase


class TestQueryEvaluator(PkbTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.expected_result = [
            "1, 3, 6, 8, 10, 12, 16, 17, 19, 20, 22, 23, 25, 29, 32, 34, 35, 36, 37",
            "3, 16, 19, 32, 37",
        ]
        self.query_evaluator = QueryEvaluator(self.pkb)

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

    def test_select_assign_that_modifies_x(self):
        # Arrange
        variables = "assign a;"
        query = "Select a such that Modifies(a,'x')"
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertIn(result, self.expected_result)

    def test_select_assign_that_modifies_v_with_var_name(self):
        # Arrange
        variables = "assign a; variable v;"
        query = "Select a such that Modifies (a,v) with v.varName='x'"
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertIn(result, self.expected_result)

    def test_select_statement_that_follows_statement(self):
        # Arrange
        variables = "stmt s1, s2;"
        query = "Select s1 such that Follows (s1, s2)"
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(
                result,
                "3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 17, 18, 19, 20, 25, 26, 27, 32",
            )

    def test_select_assign_that_is_followed_by_prog_line(self):
        # Arrange
        variables = "assign a;"
        query = "Select a such that Follows (14, a)"
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(result, "13")

    def test_select_assign_that_is_followed_by_prog_line_with_no_result(self):
        # Arrange
        variables = "assign a;"
        query = "Select a such that Follows (13, a)"
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(result, "")

    def test_select_assign_that_follows_prog_line(self):
        # Arrange
        variables = "assign a;"
        query = "Select a such that Follows (a, 13)"
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(result, "14")

    def test_select_statement_that_follows_with_prog_line(self):
        # Arrange
        variables = "stmt s1, s2;"
        query = "Select s1 such that Follows (s1, s2) with s1.stmt#= 5"
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(result, "5")

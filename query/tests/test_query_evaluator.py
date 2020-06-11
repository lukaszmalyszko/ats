from unittest.mock import patch

from query.query_evaluator import QueryEvaluator
from query.tests.mixins import PkbTestCase


class TestQueryEvaluator(PkbTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.expected_result = [
            "1, 3, 6, 8, 10, 12, 16, 17, 19, 20, 22, 23, 25, 29, 32, 34, 35, 36, 37",
            "2, 14, 17, 26, 29",
        ]
        self.query_evaluator = QueryEvaluator(self.pkb)

    def test_select_statement_that_modifies_x(self):
        # Arrange
        variables = "stmt s;"
        query = 'Select s such that Modifies(s,"x")'
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertIn(result, self.expected_result)

    def test_select_assign_that_modifies_x(self):
        # Arrange
        variables = "assign a;"
        query = 'Select a such that Modifies(a,"x")'
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertIn(result, self.expected_result)

    def test_select_assign_that_modifies_v_with_var_name(self):
        # Arrange
        variables = "assign a; variable v;"
        query = 'Select a such that Modifies (a,v) with v.varName="x"'
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
                "2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 15, 16, 17, 18, 21, 22, 23, 26",
            )

    def test_select_assign_that_is_followed_by_prog_line(self):
        # Arrange
        variables = "assign a;"
        query = "Select a such that Follows (15, a)"
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(result, "14")

    def test_select_assign_that_is_followed_by_prog_line_with_no_result(self):
        # Arrange
        variables = "assign a;"
        query = "Select a such that Follows (12, a)"
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(result, "")

    def test_select_assign_that_follows_prog_line(self):
        # Arrange
        variables = "assign a;"
        query = "Select a such that Follows (a, 12)"
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(result, "13")

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

    def test_select_statement_that_is_parent(self):
        # Arrange
        variables = "stmt s1, s2;"
        query = "Select s1 such that Parent (s1, s2)"
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(result, "9, 11, 19, 24, 27, 28")

    def test_select_statement_that_is_using_with_var_name(self):
        # Arrange
        variables = "stmt s1; variable v;"
        query = 'Select s1 such that Uses (s1, v) with v.varName="x"'
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(result, "3, 4, 6, 8, 10, 20, 25, 26, 30")

    def test_select_statement_that_modifies_and_uses(self):
        # Arrange
        variables = "stmt s1; variable v;"
        query = 'Select s1 such that Modifies(s1,"x1") and Uses(s1,"x2")'
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(result, "2, 14, 17, 26, 29")

    def test_select_statements_that_modifies(self):
        # Arrange
        variables = "stmt s1; variable v;"
        query = 'Select <s1, v> such that Modifies(s1,v) with v.varName="x"'
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(result, "2 x, 14 x, 17 x, 26 x, 29 x")

    def test_select_statement_that_is_parent_star(self):
        # Arrange
        variables = "stmt s1, s2;"
        query = "Select <s1, s2> such that Parent* (s1, s2)"
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(result,
                             "9 10, 9 11, 9 12, 9 13, 9 14, 9 15, 9 16, 9 17, 11 12, 11 13, 11 14, 11 15, 11 16, "
                             "19 20, 19 21, 19 22, 24 25, 27 28, 27 29, 27 30, 28 29, 28 30")

    def test_select_statement_that_is_parent_star_with(self):
        # Arrange
        variables = "stmt s1, s2;"
        query = "Select <s1, s2> such that Parent* (s1, s2) with s1.stmt#= 9"
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(result, "none")

    def test_select_statement_that_is_parent_star_with_first_param_condition(self):
        # Arrange
        variables = "stmt s1, s2;"
        query = "Select <s1, s2> such that Parent* (s1, s2) with s2.stmt#= 14"
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(result, "6 14, 12 14")

    def test_select_statement_that_follows_star(self):
        # Arrange
        variables = "stmt s1, s2;"
        query = "Select <s1, s2> such that Follows* (s1, s2)"
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(result,
                             "2 1, 3 1, 3 2, 4 1, 4 2, 4 3, 5 1, 5 2, 5 3, 5 4, 6 1, 6 2, 6 3, 6 4, 6 5, 7 1, 7 2, "
                             "7 3, 7 4, 7 5, 7 6, 8 1, 8 2, 8 3, 8 4, 8 5, 8 6, 8 7, 9 1, 9 2, 9 3, 9 4, 9 5, 9 6, "
                             "9 7, 9 8, 11 10, 13 12, 15 14, 16 14, 16 15, 17 10, 17 11, 18 1, 18 2, 18 3, 18 4, "
                             "18 5, 18 6, 18 7, 18 8, 18 9, 21 20, 22 20, 22 21, 23 19, 26 24")

    def test_select_line_that_calls(self):
        # Arrange
        variables = "procedure p, q;"
        query = "Select p such that Calls(p,q)"
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(result, "Draw, Enlarge, Main, PP, RR, Rotate, SS, Shrink, TT, Translate, UU")

    def test_select_statement_that_modifies(self):
        # Arrange
        variables = "stmt s;"
        query = 'Select s such that Modifies(s,"x")'
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(result, "6, 12, 105, 106, 107, 109, 116")

    def test_select_statement_that_modifies2(self):
        # Arrange
        variables = "assign a; variable v;"
        query = 'Select a such that Modifies(a,v) with v.varName="x"'
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(result, "106, 116")

    def test_select_if(self):
        # Arrange
        variables = "if ifs;"
        query = 'Select ifs such that Follows*(ifs, 166)'
        input_values = [variables, query]
        # Act & Assert
        with patch("builtins.input", side_effect=input_values):
            self.query_evaluator.load()
            result = self.query_evaluator.get_result()
            self.assertEqual(result, "163")

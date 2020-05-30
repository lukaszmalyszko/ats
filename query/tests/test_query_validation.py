from unittest import TestCase
from unittest.mock import patch

from query.query_parser.exceptions import (
    InvalidQueryException,
    InvalidQueryParamException,
)
from query.query_preprocessor import QueryPreprocessor
from query.tests.mixins import PkbTestCase


class TestQueryValidation(PkbTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.query_preprocessor = QueryPreprocessor(self.pkb)
        self.variables = "stmt s, s1; assign a, a1, a2; while w; variable v; constant c; prog_line n, n1, n2;"
        self.query = "Select s such that Modifies(s,'x')"

    def test_raise_invalid_query_exception_when_no_variable_after_select(self):
        self.query = "Select such that Modifies(s,'x')"
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryParamException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_no_select_at_the_beginning(self):
        self.query = "s such that Modifies(s,'x')"
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_variable_is_key_word(self):
        self.query = "Select Select such that Modifies(s,'x')"
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryParamException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_no_such_that_after_variable(self):
        self.query = "Select s Modifies(s, 'x')"

        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_no_that_after_such(self):
        self.query = "Select s such Modifies(s, 'x')"

        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_rel_has_no_closing_brackets(self):
        self.query = "Select s such that Modifies(s, 'x'"
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_rel_has_one_argument(self):
        self.query = "Select s such that Modifies(s)"
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_relation_is_invalid(self):
        self.query = "Select s such that Modddddifies(s, 'x')"
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_with_is_incorrect(self):
        self.query = "Select s such that Modifies(s, 'x') wiiith s.a=10"
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_with_has_no_condition(self):
        self.query = "Select s such that Modifies(s, 'x') with"
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_relation_param_is_incorrect(self):
        self.query = "Select s such that Modifies(b, 'x')"

        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryParamException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_select_param_is_incorrect(self):
        self.query = "Select b such that Modifies(s, 'x')"

        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryParamException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_uses_params_are_incorrect(self):
        self.query = "Select s such that Uses(s, b)"

        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryParamException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_parent_params_are_incorrect(self):
        self.query = "Select s such that Parent(s, 'x')"

        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryParamException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_parent_star_params_are_incorrect(self):
        self.query = "Select s such that Parent*(s, 'x')"

        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryParamException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_follows_params_are_incorrect(self):
        self.query = "Select s such that Follows(s, 'x')"

        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryParamException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_follows_star_params_are_incorrect(self):
        self.query = "Select s such that Follows*(s, 'x')"

        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryParamException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_condition_is_incorrect(self):
        self.query = "Select s such that Modifies(s, 'x') with s.a"
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_relation_has_wrong_type_of_argument(
        self,
    ):
        self.query = "Select s such that Modifies(s, s1)"
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryParamException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_query_ends_with_and(
        self,
    ):
        self.query = "Select s such that Modifies(s, v) and"
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_no_and_between_relations(
        self,
    ):
        self.query = "Select s such that Modifies(s, v) Uses(s,'x')"
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryException):
                self.query_preprocessor.get_input()


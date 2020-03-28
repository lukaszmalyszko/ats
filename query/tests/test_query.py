from unittest import TestCase
from unittest.mock import patch

from query.query_preprocessor import QueryPreprocessor, InvalidVariablesException
from query.query_validator.query_validator import InvalidQueryException


class TestQueryPreprocessor(TestCase):
    def setUp(self) -> None:
        self.query_preprocessor = QueryPreprocessor()
        self.variables = "stmt s, s1; assign a, a1, a2; while w; variable v; constant c; prog_line n, n1, n2;"
        self.query = "Select s such that Modifies(s,'x')"

    def test_returns_get_input_result(self):
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            self.assertEqual(
                self.query_preprocessor.get_input(), (self.variables, self.query)
            )

    def test_raise_invalid_variables_exception_when_no_semicolon_at_the_end(self):
        input_values = [self.variables[:-1], self.query]

        self.__then_run_patched_get_input_with_assert_raises_invalid_variables_exception(input_values)

    def test_raise_invalid_variables_exception_when_incorrect_variable_in_variables(
        self,
    ):
        self.variables = "incorrect_stmt is;"
        input_values = [self.variables, self.query]

        self.__then_run_patched_get_input_with_assert_raises_invalid_variables_exception(input_values)

    def test_raise_invalid_variables_exception_when_name_in_entity_list(self):
        self.variables = "stmt stmt, while;"
        input_values = [self.variables, self.query]

        self.__then_run_patched_get_input_with_assert_raises_invalid_variables_exception(input_values)

    def test_raise_invalid_variables_exception_when_no_name(self):
        self.variables = "stmt;"
        input_values = [self.variables, self.query]

        self.__then_run_patched_get_input_with_assert_raises_invalid_variables_exception(input_values)

    def test_raise_invalid_variables_exception_when_incorrect_sign_in_declaration(self):
        self.variables = "stmt s,;"
        input_values = [self.variables, self.query]

        self.__then_run_patched_get_input_with_assert_raises_invalid_variables_exception(input_values)

    def test_raise_invalid_variables_exception_when_incorrect_name(self):
        self.variables = "stmt 123q;"
        input_values = [self.variables, self.query]

        self.__then_run_patched_get_input_with_assert_raises_invalid_variables_exception(input_values)

    def __then_run_patched_get_input_with_assert_raises_invalid_variables_exception(self, input_values):
        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidVariablesException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_no_variable_after_select(self):
        self.query = "Select such that Modifies(s,'x')"
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryException):
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
            with self.assertRaises(InvalidQueryException):
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

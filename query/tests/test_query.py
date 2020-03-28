from unittest import TestCase
from unittest.mock import patch

from query.query_preprocessor import QueryPreprocessor, InvalidVariablesException


class TestQueryPreprocessor(TestCase):
    def setUp(self) -> None:
        self.query_preprocessor = QueryPreprocessor()
        self.expected_variables = "stmt s, s1; assign a, a1, a2; while w; if ifstat; procedure p; variable v; constant c; prog_line n, n1, n2;"
        self.expected_query = "Select s such that Modifies(s,'x')"

    def test_returns_get_input_result(self):
        input_values = [self.expected_variables, self.expected_query]

        with patch('builtins.input', side_effect=input_values):
            self.assertEqual(self.query_preprocessor.get_input(), (self.expected_variables, self.expected_query))

    def test_raise_invalid_variables_exception_when_no_semicolon_at_the_end(self):
        input_values = [self.expected_variables[:-1], self.expected_query]

        with patch('builtins.input', side_effect=input_values):
            with self.assertRaises(InvalidVariablesException):
                self.query_preprocessor.get_input()


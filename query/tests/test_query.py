from unittest import TestCase
from unittest.mock import patch

from query.query import QueryPreprocessor, InvalidVariablesException


class TestQueryPreprocessor(TestCase):
    def setUp(self) -> None:
        self.query_preprocessor = QueryPreprocessor()

    def test_returns_get_input_result(self):
        expected_variables = "stmt s;"
        expected_query = "Select s such that Modifies(s,'x')"
        input_values = [expected_variables, expected_query]

        with patch('builtins.input', side_effect=input_values):
            self.assertEqual(self.query_preprocessor.get_input(), (expected_variables, expected_query))

    def test_raise_invalid_variables_exception(self):
        expected_variables = "stmt s"
        expected_query = "Select s such that Modifies(s,'x')"
        input_values = [expected_variables, expected_query]

        with patch('builtins.input', side_effect=input_values):
            with self.assertRaises(InvalidVariablesException):
                self.query_preprocessor.get_input()


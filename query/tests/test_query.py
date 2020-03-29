from unittest import TestCase
from unittest.mock import patch


from query.query_preprocessor import QueryPreprocessor
from query.query_validator.exceptions import InvalidQueryException
from query.variables_validator.exceptions import InvalidVariablesException


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

    def test_returns_get_input_result_ignore_spaces(self):
        self.variables = " stmt  s ,  s1 ;  assign  a ,  a1 ,  a2 ;"
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            result = self.query_preprocessor.get_input()
            self.assertEqual(result, (self.variables, self.query))

    def test_raise_invalid_variables_exception_when_no_semicolon_at_the_end(self):
        input_values = [self.variables[:-1], self.query]

        self.__then_run_patched_get_input_with_assert_raises_invalid_variables_exception(
            input_values
        )

    def test_raise_invalid_variables_exception_when_incorrect_variable_in_variables(
        self,
    ):
        self.variables = "incorrect_stmt is;"
        input_values = [self.variables, self.query]

        self.__then_run_patched_get_input_with_assert_raises_invalid_variables_exception(
            input_values
        )

    def test_raise_invalid_variables_exception_when_name_in_entity_list(self):
        self.variables = "stmt stmt, while;"
        input_values = [self.variables, self.query]

        self.__then_run_patched_get_input_with_assert_raises_invalid_variables_exception(
            input_values
        )

    def test_raise_invalid_variables_exception_when_no_name(self):
        self.variables = "stmt;"
        input_values = [self.variables, self.query]

        self.__then_run_patched_get_input_with_assert_raises_invalid_variables_exception(
            input_values
        )

    def test_raise_invalid_variables_exception_when_incorrect_sign_in_declaration(self):
        self.variables = "stmt s,;"
        input_values = [self.variables, self.query]

        self.__then_run_patched_get_input_with_assert_raises_invalid_variables_exception(
            input_values
        )

    def test_raise_invalid_variables_exception_when_incorrect_name(self):
        self.variables = "stmt 123q;"
        input_values = [self.variables, self.query]

        self.__then_run_patched_get_input_with_assert_raises_invalid_variables_exception(
            input_values
        )

    def test_raise_invalid_variables_exception_when_two_values_with_same_name(self):
        self.variables = "stmt s, s;"
        input_values = [self.variables, self.query]

        self.__then_run_patched_get_input_with_assert_raises_invalid_variables_exception(
            input_values
        )

    def test_add_variables_to_entities(self):
        self.variables = "stmt s, s1; assign a, a1, a2;"
        input_values = [self.variables, self.query]
        expected_names = ["s", "s1", "a", "a1", "a2"]

        with patch("builtins.input", side_effect=input_values):
            self.query_preprocessor.get_input()
            self.__assert_names(expected_names)

    def __assert_names(self, expected_names):
        for name in expected_names:
            self.assertTrue(self.query_preprocessor.check_if_contains_variable(name))

    def __then_run_patched_get_input_with_assert_raises_invalid_variables_exception(
        self, input_values
    ):
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
            with self.assertRaises(InvalidQueryException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_select_param_is_incorrect(self):
        self.query = "Select b such that Modifies(s, 'x')"

        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_uses_params_are_incorrect(self):
        self.query = "Select s such that Uses(s, b)"

        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_parent_params_are_incorrect(self):
        self.query = "Select s such that Parent(s, 'x')"

        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_parent_star_params_are_incorrect(self):
        self.query = "Select s such that Parent*(s, 'x')"

        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_follows_params_are_incorrect(self):
        self.query = "Select s such that Follows(s, 'x')"

        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryException):
                self.query_preprocessor.get_input()

    def test_raise_invalid_query_exception_when_follows_star_params_are_incorrect(self):
        self.query = "Select s such that Follows*(s, 'x')"

        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryException):
                self.query_preprocessor.get_input()

    def test_returns_get_input_result_with_multiple_such_that(self):
        self.query = "Select s such that Modifies(s, 'x') such that Follows(s, s1) such that Uses(s, 'x')"
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            self.assertEqual(
                self.query_preprocessor.get_input(), (self.variables, self.query)
            )

    def test_raise_invalid_query_exception_when_condition_is_incorrect(self):
        self.query = "Select s such that Modifies(s, 'x') with s.a"
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            with self.assertRaises(InvalidQueryException):
                self.query_preprocessor.get_input()

    def test_returns_get_input_result_with_multiple_spaces(self):
        self.query = "Select   s  such    that  Modifies  ( s,   'x' )"
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            self.assertEqual(
                self.query_preprocessor.get_input(), (self.variables, self.query)
            )

    def test_build_tree_creates_tree_node(self):
        input_values = [self.variables, self.query]

        with patch("builtins.input", side_effect=input_values):
            self.query_preprocessor.get_input()
            self.query_preprocessor.build_tree()
            self.assertTrue(self.query_preprocessor.tree.root)

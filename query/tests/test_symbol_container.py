from unittest import TestCase

from query.declarations_parser.declarations_elements import Stmt
from query.declarations_parser.symbol_container import SymbolContainer


class TestSymbolContainer(TestCase):
    def setUp(self) -> None:
        self.symbol_container = SymbolContainer()
        self.symbol = Stmt("test")
        self.symbol2 = Stmt("test2")
        self.symbol_container.entities = {"stmt": [self.symbol, self.symbol2]}

    def test_return_true_if_symbol_name_is_var_name(self):
        self.assertTrue(self.symbol_container.check_if_contains_symbol("test"))

    def test_return_false_if_symbol_name_is_not_var_name(self):
        self.assertFalse(self.symbol_container.check_if_contains_symbol("wrong"))

    def test_return_true_if_symbol_name_and_type_compare_with_given(self):
        self.assertTrue(self.symbol_container.check_if_contains_symbol("test", "stmt"))

    def test_return_false_if_symbol_type_not_compare_with_given(self):
        self.assertFalse(self.symbol_container.check_if_contains_symbol("test", "ref"))

    def test_return_symbol_when_name_compare_with_given(self):
        self.assertEqual(self.symbol_container.get_symbol("test"), self.symbol)

    def test_return_false_when_no_symbols_with_name_like_given(self):
        self.assertNotEqual(self.symbol_container.get_symbol("test3"), self.symbol)

from query.query_parser.query_builder import QueryBuilder
from query.declarations_parser.symbol_container import SymbolContainer
from query.declarations_parser.declarations_validator import DeclarationsValidator


class QueryPreprocessor:
    def __init__(self):
        self.declarations = ""
        self.query = ""
        self.symbols = SymbolContainer()
        self.tree = None

    def get_input(self):
        self.declarations = self._get_declarations()
        self.query = self._get_query()

        return self.declarations, self.query

    def _get_query(self):
        query_input = input("Podaj zapytanie: ")
        query = self.__build_query(query_input)
        return query

    def _get_declarations(self):
        declarations_input = input("Podaj deklaracje: ")
        declarations = self.__prepare_and_validate_declarations(declarations_input)
        return declarations

    def __prepare_and_validate_declarations(self, declarations_input):
        declarations_validator = DeclarationsValidator()
        self.symbols.entities = declarations_validator.validate_declarations(
            declarations_input
        )

        return declarations_input

    def __build_query(self, query_input):
        query_builder = QueryBuilder(self)
        self.tree = query_builder.build_query(query_input)
        return query_input

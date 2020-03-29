from query.query_parser import QueryParser
from query.query_validator.exceptions import InvalidQueryException


class QueryValidator(QueryParser):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)

    def validate_query(self, query_string):
        query_elements = self.parse_query(query_string)
        for element in query_elements:
            self.expected_element.validate(element)
            self.expected_element = self.expected_element.next(self.query_preprocessor)
        self.__check_if_query_is_finished()

    def __check_if_query_is_finished(self):
        if not self.expected_element.can_query_be_finished():
            raise InvalidQueryException("# Niepoprawne zakończenie zapytania")

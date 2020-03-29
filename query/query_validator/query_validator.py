from query.query_validator.exceptions import InvalidQueryException
from query.query_validator.query_elements import Select, Element


class QueryValidator:
    def __init__(self, query_preprocessor):
        self.query_preprocessor = query_preprocessor
        self.expected_element = Select(self.query_preprocessor)

    def validate_query(self, query_string):
        query_elements = self.__get_query_elements(query_string)
        for element in query_elements:
            self.expected_element.validate(element)
            self.expected_element = self.expected_element.next(self.query_preprocessor)
        self.__check_if_query_is_finished()

    def __get_query_elements(self, query_string):
        elements = []
        buffer = ""
        relation = False
        for char in query_string:
            if char == "(":
                relation = True
            if char == ")":
                relation = False
            if buffer.endswith(" ") and relation is False:
                elements.append(buffer)
                buffer = ""
            buffer = buffer + char
        elements.append(buffer)
        elements = [element.strip(" ") for element in elements]
        return elements

    def __check_if_query_is_finished(self):
        if not self.expected_element.can_query_be_finished():
            raise InvalidQueryException("# Niepoprawne zakończenie zapytania")

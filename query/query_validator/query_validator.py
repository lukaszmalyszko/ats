import re

from query.query_validator.exceptions import InvalidQueryException
from query.query_validator.query_elements import Select
from query.utils import CONDITION


class QueryValidator:
    def __init__(self, query_preprocessor):
        self.query_preprocessor = query_preprocessor
        self.expected_element = Select(self.query_preprocessor)

    def validate_query(self, query_string):
        query_elements = self.__parse_query(query_string)
        for element in query_elements:
            self.expected_element.validate(element)
            self.expected_element = self.expected_element.next(self.query_preprocessor)
        self.__check_if_query_is_finished()

    def __parse_query(self, query_string):
        elements = []
        buffer = ""
        relation = False
        condition = False
        for char in query_string:
            if "with" in buffer:
                condition = True
                elements.append(buffer)
                buffer = ""
                continue
            if char == "(":
                relation = True
            if char != " " and buffer.endswith(" ") and not relation and not condition:
                elements.append(buffer)
                buffer = ""
            if condition:
                if re.match(CONDITION, buffer) and buffer.endswith(" "):
                    condition = False
            if char == ")":
                relation = False
            buffer = buffer + char
        elements.append(buffer)
        elements = [element.strip(" ") for element in elements]
        return elements

    def __check_if_query_is_finished(self):
        if not self.expected_element.can_query_be_finished():
            raise InvalidQueryException("# Niepoprawne zakończenie zapytania")

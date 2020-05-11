import re

from query.query_parser.query_elements import Select
from query.utils import CONDITION


class QueryParser:
    def __init__(self, query_preprocessor):
        self.query_preprocessor = query_preprocessor
        self.expected_element = Select(self.query_preprocessor)

    @staticmethod
    def parse_query(query_string):
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

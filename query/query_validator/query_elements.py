import re

KEY_WORDS = [
    "Select",
    "such",
    "that",
    "with",
]

IDENT = "^[a-zA-Z][a-zA-Z0-9#]*$"


class Element:
    def __init__(self):
        self.value = []
        self.error_message = ""
        self.expected_element = Element

    def validate(self, value):
        return True


class Select(Element):
    def __init__(self):
        super().__init__()
        self.value = ["Select"]
        self.error_message = '# Zapytanie nie zaczyna się od "Select"'
        self.expected_element = Variable

    def validate(self, value):
        return value in self.value


class Variable(Element):
    def __init__(self):
        super().__init__()
        self.value = []
        self.error_message = "# Oczekiwana poprawna nazwa elementu"
        self.expected_element = Element

    def validate(self, value):
        return re.match(IDENT, value) and value not in KEY_WORDS

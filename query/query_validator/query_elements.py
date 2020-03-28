import re

KEY_WORDS = [
    "Select",
    "such",
    "that",
    "with",
    "stmt",
    "while",
    "assign",
    "prog_line",
    "constant",
    "variable",
]

RELATIONS = (
    "Modifies",
    "Uses",
    "Parent",
    "Parent*",
    "Follows",
    "Follows*",
)

IDENT = "[a-zA-Z][a-zA-Z0-9#]*"
STMT_REF = f"({IDENT})|[_]|[0-9]+"
ENT_REF = f"({IDENT})|[_]|['\"]({IDENT}['\"])"
PARAM_REF = f"({IDENT})|[_]|[0-9]+|['\"]({IDENT}['\"])"
REL_REF = f"[a-zA-Z]+[(]({PARAM_REF})+[ ]*[,][ ]*({PARAM_REF})+[)]"


class Element:
    def __init__(self):
        self.value = []
        self.error_message = ""
        self._next = Element

    def validate(self, value):
        return True

    def get_next_element(self):
        return self._next()


class Select(Element):
    def __init__(self):
        super().__init__()
        self.value = ["Select"]
        self.error_message = '# Zapytanie nie zaczyna się od "Select"'
        self.next = Variable

    def validate(self, value):
        if value not in self.value:
            raise InvalidQueryException(self.error_message)


class Variable(Element):
    def __init__(self):
        super().__init__()
        self.value = []
        self.error_message = "# Oczekiwana poprawna nazwa elementu"
        self.next = Such

    def validate(self, value):
        if not re.match(IDENT, value) or value in KEY_WORDS:
            raise InvalidQueryException(self.error_message)


class Such(Element):
    def __init__(self):
        super().__init__()
        self.value = ["such"]
        self.error_message = '# Oczekiwana klauzula "such that"'
        self.next = That

    def validate(self, value):
        if value not in self.value:
            raise InvalidQueryException(self.error_message)


class That(Element):
    def __init__(self):
        super().__init__()
        self.value = ["that"]
        self.error_message = '# Niepoprawna klauzula "such that"'
        self.next = Relation

    def validate(self, value):
        if value not in self.value:
            raise InvalidQueryException(self.error_message)


class Relation(Element):
    def __init__(self):
        super().__init__()
        self.value = []
        self.error_message = "# Niepoprawna składnia relacji"
        self.next = Element  # TODO w przyszłości zmiana na with

    def validate(self, value):
        relation = list(filter(value.startswith, RELATIONS))
        if not relation or not self._is_params_syntax_correct(value):
            raise InvalidQueryException(self.error_message)

    def _is_params_syntax_correct(self, value):
        return re.match(REL_REF, value)


class Modifies(Relation):
    def __init__(self):
        super().__init__()
        self.error_message = "# Niepoprawna składnia Modifies"
        self.next = Element  # w przyszłości zmiana na with


class Uses(Relation):
    def __init__(self):
        super().__init__()
        self.error_message = "# Niepoprawna składnia Uses"
        self.next = Element  # w przyszłości zmiana na with


class Parent(Relation):
    def __init__(self):
        super().__init__()
        self.error_message = "# Niepoprawna składnia Parent"
        self.next = Element  # w przyszłości zmiana na with


class ParentStar(Relation):
    def __init__(self):
        super().__init__()
        self.error_message = "# Niepoprawna składnia Parent*"
        self.next = Element  # w przyszłości zmiana na with


class Follows(Relation):
    def __init__(self):
        super().__init__()
        self.error_message = "# Niepoprawna składnia Follows"
        self.next = Element  # w przyszłości zmiana na with


class FollowsStar(Relation):
    def __init__(self):
        super().__init__()
        self.error_message = "# Niepoprawna składnia Follows*"
        self.next = Element  # w przyszłości zmiana na with


class InvalidQueryException(Exception):
    def __init(self, message):
        self.message = message

import re
from abc import abstractmethod

from query.query_parser.exceptions import InvalidQueryException
from query.query_parser.params_validator import ParamsValidator
from query.query_tree.tree_nodes import (
    SelectNode,
    ModifiesNode,
    UsesNode,
    ParentNode,
    ParentStarNode,
    FollowsNode,
    FollowsStarNode,
    ConditionNode,
)
from query.utils import REL_REF, CONDITION


class Element:
    def __init__(self, query_preprocessor):
        self.query_preprocessor = query_preprocessor
        self.value = []
        self.error_message = "# Błąd w zapytaniu"
        self.next = Element

    def validate(self, value):
        element = [
            element
            for element in CONSTRUCTION_TO_NEXT_MAPPING.keys()
            if element == value
        ]
        if not element:
            raise InvalidQueryException(self.error_message)
        self.next = CONSTRUCTION_TO_NEXT_MAPPING[element[0]]
        return True

    def can_query_be_finished(self):
        return True

    @abstractmethod
    def create_node(self, value, tree):
        pass


class Select(Element):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.value = ["Select"]
        self.error_message = '# Zapytanie nie zaczyna się od "Select"'
        self.next = Variable

    def validate(self, value):
        if value not in self.value:
            raise InvalidQueryException(self.error_message)

    def can_query_be_finished(self):
        return False

    def create_node(self, value, tree):
        pass


class Variable(Element):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.value = []
        self.error_message = "# Oczekiwana poprawna nazwa elementu"
        self.next = Element

    def validate(self, value):
        does_variable_exist = ParamsValidator.get_variable_ref(
            value, self.query_preprocessor
        )
        if not does_variable_exist:
            raise InvalidQueryException(self.error_message)

    def can_query_be_finished(self):
        return False

    def create_node(self, value, tree):
        select = SelectNode()
        variable = self.query_preprocessor.symbols.get_symbol(value)
        select.add_variable(variable)
        tree.set_select(select)


class Such(Element):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.value = ["such"]
        self.error_message = '# Oczekiwana klauzula "such that"'
        self.next = That

    def validate(self, value):
        if value not in self.value:
            raise InvalidQueryException(self.error_message)

    def can_query_be_finished(self):
        return False

    def create_node(self, value, tree):
        pass


class That(Element):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.value = ["that"]
        self.error_message = '# Niepoprawna klauzula "such that"'
        self.next = Relation

    def validate(self, value):
        if value not in self.value:
            raise InvalidQueryException(self.error_message)

    def can_query_be_finished(self):
        return False

    def create_node(self, value, tree):
        pass


class Relation(Element):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.value = []
        self.error_message = "# Niepoprawna składnia relacji"
        self.next = Element  # TODO w przyszłości zmiana na with

        self.first_param = ""
        self.second_param = ""

    def validate(self, value):
        relation = list(filter(value.startswith, RELATION_TO_MODEL.keys()))
        if not relation or not self._is_params_syntax_correct(value):
            raise InvalidQueryException(self.error_message)
        else:
            model = RELATION_TO_MODEL[relation[-1]](self.query_preprocessor)
            model.extract_params(value)
            model.validate_params()

    def extract_params(self, value):
        buffer = ""
        first_param = False
        second_param = False
        for char in value:
            if "(" in char:
                first_param = True
                continue
            if "," in char:
                self.first_param = buffer.strip(" ")
                buffer = ""
                first_param = False
                second_param = True
                continue
            if ")" in char:
                self.second_param = buffer.strip(" ")
                second_param = False
                continue
            if first_param is True or second_param is True:
                buffer = buffer + char

    @abstractmethod
    def validate_params(self):
        pass

    def can_query_be_finished(self):
        return False

    def _is_params_syntax_correct(self, value):
        return re.match(REL_REF, value)

    def create_node(self, value, tree):
        relation = list(filter(value.startswith, RELATION_TO_MODEL.keys()))
        model = RELATION_TO_MODEL[relation[-1]](self.query_preprocessor)
        model.extract_params(value)
        model.validate_params()
        model.create_node(value, tree)


class Modifies(Relation):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.error_message = "# Niepoprawna składnia Modifies"
        self.next = Element

    def validate_params(self):
        # Modifies(stmtRef, entRef)
        self.first_param = ParamsValidator.get_statement_ref(
            self.first_param, self.query_preprocessor
        )
        self.second_param = ParamsValidator.get_entity_ref(
            self.second_param, self.query_preprocessor
        )

    def create_node(self, value, tree):
        modifies_node = ModifiesNode()
        modifies_node.first_arg = self.first_param
        modifies_node.second_arg = self.second_param
        tree.add_such_that(modifies_node)


class Uses(Relation):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.error_message = "# Niepoprawna składnia Uses"
        self.next = Element

    def validate_params(self):
        # Uses(stmtRef, entRef)
        self.first_param = ParamsValidator.get_statement_ref(
            self.first_param, self.query_preprocessor
        )
        self.second_param = ParamsValidator.get_entity_ref(
            self.second_param, self.query_preprocessor
        )

    def create_node(self, value, tree):
        uses_node = UsesNode()
        uses_node.first_arg = self.first_param
        uses_node.second_arg = self.second_param
        tree.add_such_that(uses_node)


class Parent(Relation):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.error_message = "# Niepoprawna składnia Parent"
        self.next = Element

    def validate_params(self):
        # Parent(stmtRef, stmtRef)
        self.first_param = ParamsValidator.get_statement_ref(
            self.first_param, self.query_preprocessor
        )
        self.second_param = ParamsValidator.get_statement_ref(
            self.second_param, self.query_preprocessor
        )

    def create_node(self, value, tree):
        parent_node = ParentNode()
        parent_node.first_arg = self.first_param
        parent_node.second_arg = self.second_param
        tree.add_such_that(parent_node)


class ParentStar(Relation):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.error_message = "# Niepoprawna składnia Parent*"
        self.next = Element

    def validate_params(self):
        # Parent*(stmtRef, stmtRef)
        self.first_param = ParamsValidator.get_statement_ref(
            self.first_param, self.query_preprocessor
        )
        self.second_param = ParamsValidator.get_statement_ref(
            self.second_param, self.query_preprocessor
        )

    def create_node(self, value, tree):
        parent_star_node = ParentStarNode()
        parent_star_node.first_arg = self.first_param
        parent_star_node.second_arg = self.second_param
        tree.add_such_that(parent_star_node)


class Follows(Relation):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.error_message = "# Niepoprawna składnia Follows"
        self.next = Element

    def validate_params(self):
        # Follows(stmtRef, stmtRef)
        self.first_param = ParamsValidator.get_statement_ref(
            self.first_param, self.query_preprocessor
        )
        self.second_param = ParamsValidator.get_statement_ref(
            self.second_param, self.query_preprocessor
        )

    def create_node(self, value, tree):
        follows_node = FollowsNode()
        follows_node.first_arg = self.first_param
        follows_node.second_arg = self.second_param
        tree.add_such_that(follows_node)


class FollowsStar(Relation):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.error_message = "# Niepoprawna składnia Follows*"
        self.next = Element

    def validate_params(self):
        # Follows*(stmtRef, stmtRef)
        self.first_param = ParamsValidator.get_statement_ref(
            self.first_param, self.query_preprocessor
        )
        self.second_param = ParamsValidator.get_statement_ref(
            self.second_param, self.query_preprocessor
        )

    def create_node(self, value, tree):
        follows_star_node = FollowsStarNode()
        follows_star_node.first_arg = self.first_param
        follows_star_node.second_arg = self.second_param
        tree.add_such_that(follows_star_node)


class Condition(Element):
    def __init__(self, query_preprocessor):
        super().__init__(query_preprocessor)
        self.error_message = "# Niepoprawna składnia warunku"
        self.first_arg = ""
        self.attr_name = ""
        self.second_arg = ""
        self.next = Element

    def validate(self, value):
        if not re.match(CONDITION, value):
            raise InvalidQueryException(self.error_message)
        self.extract_args(value)
        self.first_arg, self.attr_name = ParamsValidator.get_condition_variable(self.first_arg, self.query_preprocessor)
        self.second_arg = ParamsValidator.get_condition_value(self.second_arg)
        # na podstawie typu ref
        # TODO attributes validation

    def can_query_be_finished(self):
        return False

    def extract_args(self, value):
        buffer = ""
        for char in value:
            if "=" in char:
                self.first_arg = buffer.strip(" ")
                buffer = ""
                continue
            buffer = buffer + char
        self.second_arg = buffer.strip(" ")

    def create_node(self, value, tree):
        condition_node = ConditionNode()
        condition_node.first_arg = self.first_arg
        condition_node.second_arg = self.second_arg
        condition_node.attr_name = self.attr_name
        tree.add_with(condition_node)
        pass


RELATION_TO_MODEL = {
    "Modifies": Modifies,
    "Uses": Uses,
    "Parent": Parent,
    "Parent*": ParentStar,
    "Follows": Follows,
    "Follows*": FollowsStar,
}

CONSTRUCTION_TO_NEXT_MAPPING = {
    "Select": Variable,
    "such": That,
    "that": Relation,
    "pattern": None,
    "with": Condition,
}

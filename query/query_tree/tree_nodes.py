from abc import abstractmethod, ABC

from query.declarations_parser.declarations_elements import (
    Stmt,
    While,
    Assign,
    Variable,
    ProgLine,
    Ref,
)

MAP_CLASS_TO_GET_METHOD = {
    Stmt: "get_stmt_map",
    While: "get_while_map",
    Assign: "get_assign_map",
    Variable: "get_variables_map",
    ProgLine: "get_nodes_map",
}

MAP_ATTR_NAME_TO_NODE_ATTRIBUTE = {"varName": "get_name", "stmt#": "get_line"}


class Node(ABC):
    def __init__(self):
        self._child = None
        self._parent = None
        self._sibling = None

    def set_child(self, node):
        self._child = node

    def set_parent(self, node):
        self._parent = node

    def set_sibling(self, node):
        self._sibling = node

    @property
    def child(self):
        return self._child

    @property
    def parent(self):
        return self._parent

    @property
    def sibling(self):
        return self._sibling


class SelectNode(Node):
    def __init__(self):
        super().__init__()
        self._variables = []

    @property
    def variables(self):
        return self._variables

    def add_variable(self, node):
        self._variables.append(node)

    def evaluate(self, pkb):
        raise NotImplementedError


class RelationNode(Node):
    def __init__(self):
        super().__init__()
        self._first_arg = None
        self._second_arg = None

    @property
    def first_arg(self):
        return self._first_arg

    @first_arg.setter
    def first_arg(self, node):
        self._first_arg = node

    @property
    def second_arg(self):
        return self._second_arg

    @second_arg.setter
    def second_arg(self, node):
        self._second_arg = node


class ModifiesNode(RelationNode):
    def __init__(self):
        super().__init__()

    def evaluate(self, pkb, with_stmt):
        result = []
        get_method = MAP_CLASS_TO_GET_METHOD[self.first_arg.__class__]
        stmt_map = getattr(pkb, get_method)()

        for stmt in with_stmt:
            if stmt.first_arg == self.second_arg:
                self.second_arg = stmt.second_arg

        for index, node in stmt_map.items():
            if pkb.isModifing(index, self.second_arg):
                result.append(node.get_line())
        return result


class UsesNode(RelationNode):
    def __init__(self):
        super().__init__()


class ParentNode(RelationNode):
    def __init__(self):
        super().__init__()


class ParentStarNode(RelationNode):
    def __init__(self):
        super().__init__()


class FollowsNode(RelationNode):
    def __init__(self):
        super().__init__()

    def evaluate(self, pkb, with_stmt):
        result = []
        get_first_arg_method = MAP_CLASS_TO_GET_METHOD.get(self.first_arg.__class__, "")
        get_second_arg_method = MAP_CLASS_TO_GET_METHOD.get(
            self.second_arg.__class__, ""
        )
        if isinstance(self.first_arg, int):
            first_arg_map = pkb.get_node_with_index(self.first_arg)
        else:
            first_arg_map = getattr(pkb, get_first_arg_method)()
        if isinstance(self.second_arg, int):
            second_arg_map = pkb.get_node_with_index(self.second_arg)
        else:
            second_arg_map = getattr(pkb, get_second_arg_method)()
        for stmt in with_stmt:
            # jeżeli with dotyczy pierwszego argumentu
            if stmt.first_arg == self.first_arg:
                first_arg_map = stmt.evaluate(first_arg_map)
            if stmt.first_arg == self.second_arg:
                second_arg_map = stmt.evaluate(second_arg_map)
        for first_index, first_node in first_arg_map.items():
            for second_index, second_node in second_arg_map.items():
                if pkb.isFollowing(first_index, second_index):
                    if self.parent.is_selected(self.first_arg):
                        result.append(first_node.get_line())
                    if self.parent.is_selected(self.second_arg):
                        result.append(second_node.get_line())
        return result


class FollowsStarNode(RelationNode):
    def __init__(self):
        super().__init__()

    def evaluate(self, pkb, with_stmt):
        result = []
        get_first_arg_method = MAP_CLASS_TO_GET_METHOD.get(self.first_arg.__class__, "")
        get_second_arg_method = MAP_CLASS_TO_GET_METHOD.get(
            self.second_arg.__class__, ""
        )
        if isinstance(self.first_arg, int):
            first_arg_map = pkb.get_node_with_index(self.first_arg)
        else:
            first_arg_map = getattr(pkb, get_first_arg_method)()
        if isinstance(self.second_arg, int):
            second_arg_map = pkb.get_node_with_index(self.second_arg)
        else:
            second_arg_map = getattr(pkb, get_second_arg_method)()
        for stmt in with_stmt:
            if stmt.first_arg == self.second_arg:
                self.second_arg = stmt.second_arg
        for first_index, first_node in first_arg_map.items():
            for second_index, second_node in second_arg_map.items():
                if pkb.isFollowing(first_index, second_index):
                    if self.parent.is_selected(self.first_arg):
                        result.append(first_node.get_line())
                    if self.parent.is_selected(self.second_arg):
                        result.append(second_node.get_line())
        return result


class ConditionNode(Node):
    def __init__(self):
        super().__init__()
        self._first_arg = None
        self._second_arg = None
        self._attr_name = ""

    @property
    def first_arg(self):
        return self._first_arg

    @first_arg.setter
    def first_arg(self, node):
        self._first_arg = node

    @property
    def second_arg(self):
        return self._second_arg

    @second_arg.setter
    def second_arg(self, node):
        self._second_arg = node

    @property
    def attr_name(self):
        return self._attr_name

    @attr_name.setter
    def attr_name(self, node):
        self._attr_name = node

    def evaluate(self, dict_to_filter):
        result = {}
        attr = MAP_ATTR_NAME_TO_NODE_ATTRIBUTE[self.attr_name]
        for index, node in dict_to_filter.items():
            if getattr(node, attr)() == self.second_arg:
                result[index] = node
        return result


class PatternNode(Node):
    def __init__(self):
        # TODO pattern implementation
        super().__init__()

    def evaluate(self, pkb):
        pass

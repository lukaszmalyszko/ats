from abc import abstractmethod, ABC

from query.declarations_parser.declarations_elements import Stmt, While, Assign, Variable, ProgLine

MAP_CLASS_TO_GET_METHOD = {
    Stmt: "get_stmt_map",
    While: "get_while_map",
    Assign: "get_assign_map",
    Variable: "get_variables_map",
    ProgLine: "get_nodes_map",

}


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

    @abstractmethod
    def evaluate(self, pkb):
        pass


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

    def evaluate(self, pkb):
        pass


class ModifiesNode(RelationNode):
    def __init__(self):
        super().__init__()

    def evaluate(self, pkb):
        result = []
        get_method = MAP_CLASS_TO_GET_METHOD[self.first_arg.__class__]
        stmt_map = getattr(pkb, get_method)()
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


class FollowsStarNode(RelationNode):
    def __init__(self):
        super().__init__()


class ConditionNode(Node):
    def __init__(self):
        super().__init__()
        self._first_attr = None
        self._second_attr = None

    @property
    def first_attr(self):
        return self._first_attr

    @first_attr.setter
    def first_attr(self, node):
        self._first_attr = node

    @property
    def second_attr(self):
        return self._second_attr

    @second_attr.setter
    def second_attr(self, node):
        self._second_attr = node

    def evaluate(self, pkb):
        pass


class PatternNode(Node):
    def __init__(self):
        # TODO pattern implementation
        super().__init__()

    def evaluate(self, pkb):
        pass

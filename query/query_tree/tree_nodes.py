class Node:
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


class SuchThatNode(Node):
    def __init__(self):
        super().__init__()


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


class WithNode(Node):
    def __init__(self):
        super().__init__()


class ConditionNode(Node):
    def __init__(self):
        super().__init__()
        self._first_attr = None
        self._second_attr = None


class PatternNode(Node):
    def __init__(self):
        # TODO pattern implementation
        super().__init__()

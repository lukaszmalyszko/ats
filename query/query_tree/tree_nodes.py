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


class Root:
    def __init__(self):
        self._select = None
        self._result = None
        self._statements = {
            SuchThatNode: [],
            WithNode: [],
            PatternNode: [],
        }

    @property
    def select(self):
        return self._select

    @select.setter
    def select(self, node):
        self._select = node

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, node):
        self._result = node


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

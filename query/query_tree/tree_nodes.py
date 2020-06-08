from abc import ABC

from ast_ import NodeType
from query.declarations_parser.declarations_elements import (
    Stmt,
    While,
    Assign,
    Variable,
    ProgLine,
    Ref, Procedure,
)

MAP_CLASS_TO_GET_METHOD = {
    Stmt: "get_stmt_map",
    While: "get_while_map",
    Assign: "get_assign_map",
    Variable: "get_variables_map",
    ProgLine: "get_nodes_map",
    Procedure: "get_nodes_map",
}

MAP_ATTR_NAME_TO_NODE_ATTRIBUTE = {"varName": "get_value", "stmt#": "get_line"}


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
        self._first_arg_result = []
        self._second_arg_result = []

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

    def get_arguments(self, pkb, with_stmt, previous_result=None, grand_parent=None):
        first_args = None
        second_args = None
        if previous_result:
            first_args = previous_result.get(self.first_arg)
            second_args = previous_result.get(self.second_arg)
        if not first_args:
            first_args = {}
            get_first_arg_method = MAP_CLASS_TO_GET_METHOD.get(self.first_arg.__class__, "")
            if isinstance(self.first_arg, int):
                first_args = [pkb.get_node_with_index(self.first_arg)]
            elif isinstance(self.first_arg, str):
                first_args = [pkb.get_node_with_value(self.first_arg)]
            elif get_first_arg_method:
                first_args = [{key: value} for key, value in getattr(pkb, get_first_arg_method)().items()]
        if not second_args:
            second_args = {}
            get_second_arg_method = MAP_CLASS_TO_GET_METHOD.get(
                self.second_arg.__class__, ""
            )
            if isinstance(self.second_arg, int):
                second_args = [pkb.get_node_with_index(self.second_arg)]
            elif isinstance(self.second_arg, str):
                second_args = [pkb.get_node_with_value(self.second_arg)]
            elif get_second_arg_method:
                second_args = [{key: value} for key, value in getattr(pkb, get_second_arg_method)().items()]
        if not grand_parent:
            for stmt in with_stmt:
                if stmt.first_arg == self.first_arg:
                    first_args = stmt.evaluate(first_args)
                if stmt.first_arg == self.second_arg:
                    second_args = stmt.evaluate(second_args)

        return first_args, second_args


class ModifiesNode(RelationNode):
    def __init__(self):
        super().__init__()

    def evaluate(self, pkb, with_stmt, previous_result=None):
        first_args, second_args = self.get_arguments(pkb, with_stmt, previous_result)

        for first_arg in first_args:
            first_index, first_node = list(first_arg.items())[0]
            for second_arg in second_args:
                second_index, second_node = list(second_arg.items())[0]
                if pkb.isModifing(first_index, second_node.get_value()):
                    self._first_arg_result.append({first_index: first_node})
                    self._second_arg_result.append({second_index: second_node})
        return {
            self.first_arg: self._first_arg_result,
            self.second_arg: self._second_arg_result,
        }


class UsesNode(RelationNode):
    def __init__(self):
        super().__init__()

    def evaluate(self, pkb, with_stmt, previous_result=None):
        first_args, second_args = self.get_arguments(pkb, with_stmt, previous_result)

        for first_arg in first_args:
            first_index, first_node = list(first_arg.items())[0]
            for second_arg in second_args:
                second_index, second_node = list(second_arg.items())[0]
                if pkb.isUsing(first_index, second_node.get_value()):
                    self._first_arg_result.append({first_index: first_node})
                    self._second_arg_result.append({second_index: second_node})
        return {
            self.first_arg: self._first_arg_result,
            self.second_arg: self._second_arg_result,
        }


class ParentNode(RelationNode):
    def __init__(self):
        super().__init__()

    def evaluate(self, pkb, with_stmt, previous_result=None):
        first_args, second_args = self.get_arguments(pkb, with_stmt, previous_result)

        for first_arg in first_args:
            first_index, first_node = list(first_arg.items())[0]
            for second_arg in second_args:
                second_index, second_node = list(second_arg.items())[0]
                if pkb.isParent(first_index, second_index):
                    self._first_arg_result.append({first_index: first_node})
                    self._second_arg_result.append({second_index: second_node})
        return {
            self.first_arg: self._first_arg_result,
            self.second_arg: self._second_arg_result,
        }


class ParentStarNode(RelationNode):
    def __init__(self, grand_parent=None):
        super().__init__()
        self._grand_parent = grand_parent

    def evaluate(self, pkb, with_stmt, previous_result=None):
        total_result = {
            self.first_arg: [],
            self.second_arg: [],
        }
        first_args, second_args = self.get_arguments(pkb, with_stmt, previous_result, self._grand_parent)
        second_args = [{key: value} for key, value in pkb.get_nodes_map().items()]

        for first_arg in first_args:
            first_index, first_node = list(first_arg.items())[0]
            for second_arg in second_args:
                second_index, second_node = list(second_arg.items())[0]
                if pkb.isParent(first_index, second_index):
                    if self._grand_parent:
                        grand_index, grand_node = list(self._grand_parent.items())[0]
                        self._first_arg_result.append({grand_index: grand_node})
                        self._second_arg_result.append({second_index: second_node})
                    self._first_arg_result.append({first_index: first_node})
                    self._second_arg_result.append({second_index: second_node})
                    result = {
                        self.first_arg: [{second_index: second_node}],
                        self.second_arg: [],
                    }
                    parent_star_node = ParentStarNode(self._grand_parent or first_arg)
                    parent_star_node.first_arg = self.first_arg
                    parent_star_node.second_arg = self.second_arg
                    result = parent_star_node.evaluate(pkb, with_stmt, result)
                    if result:
                        self._first_arg_result = self._first_arg_result + result[self.first_arg]
                        self._second_arg_result = self._second_arg_result + result[self._second_arg]
        if not len(self._first_arg_result):
            return None
        first_arg_result = []
        second_arg_result = []
        for result in zip(self._first_arg_result, self._second_arg_result):
            correct = True
            for stmt in with_stmt:
                if stmt.first_arg == self.first_arg:
                    correct = stmt.evaluate_node(list(result[0].values())[0])
                if stmt.first_arg == self.second_arg:
                    correct = stmt.evaluate_node(list(result[1].values())[0])
            if correct:
                first_arg_result.append(result[0])
                second_arg_result.append(result[1])
        total_result[self.first_arg] = total_result[self.first_arg] + first_arg_result
        total_result[self.second_arg] = total_result[self.second_arg] + second_arg_result
        return total_result


class FollowsNode(RelationNode):
    def __init__(self):
        super().__init__()

    def evaluate(self, pkb, with_stmt, previous_result=None):
        first_args, second_args = self.get_arguments(pkb, with_stmt, previous_result)

        for first_arg in first_args:
            first_index, first_node = list(first_arg.items())[0]
            for second_arg in second_args:
                second_index, second_node = list(second_arg.items())[0]
                if pkb.isFollowing(first_index, second_index):
                    self._first_arg_result.append({first_index: first_node})
                    self._second_arg_result.append({second_index: second_node})
        return {
            self.first_arg: self._first_arg_result,
            self.second_arg: self._second_arg_result,
        }


class FollowsStarNode(RelationNode):
    def __init__(self, grand_parent=None):
        super().__init__()
        self._grand_parent = grand_parent

    def evaluate(self, pkb, with_stmt, previous_result=None):
        total_result = {
            self.first_arg: [],
            self.second_arg: [],
        }
        first_args, second_args = self.get_arguments(pkb, with_stmt, previous_result, self._grand_parent)
        second_args = [{key: value} for key, value in pkb.get_nodes_map().items()]

        for first_arg in first_args:
            first_index, first_node = list(first_arg.items())[0]
            for second_arg in second_args:
                second_index, second_node = list(second_arg.items())[0]
                if pkb.isFollowing(first_index, second_index):
                    if self._grand_parent:
                        grand_index, grand_node = list(self._grand_parent.items())[0]
                        self._first_arg_result.append({grand_index: grand_node})
                        self._second_arg_result.append({second_index: second_node})
                    self._first_arg_result.append({first_index: first_node})
                    self._second_arg_result.append({second_index: second_node})
                    result = {
                        self.first_arg: [{second_index: second_node}],
                        self.second_arg: [],
                    }
                    follows_star_node = FollowsStarNode(self._grand_parent or first_arg)
                    follows_star_node.first_arg = self.first_arg
                    follows_star_node.second_arg = self.second_arg
                    result = follows_star_node.evaluate(pkb, with_stmt, result)
                    if result:
                        self._first_arg_result = self._first_arg_result + result[self.first_arg]
                        self._second_arg_result = self._second_arg_result + result[self._second_arg]
        if not len(self._first_arg_result):
            return None
        first_arg_result = []
        second_arg_result = []
        for result in zip(self._first_arg_result, self._second_arg_result):
            correct = True
            for stmt in with_stmt:
                if stmt.first_arg == self.first_arg:
                    correct = stmt.evaluate_node(list(result[0].values())[0])
                if stmt.first_arg == self.second_arg:
                    correct = stmt.evaluate_node(list(result[1].values())[0])
            if correct:
                first_arg_result.append(result[0])
                second_arg_result.append(result[1])
        total_result[self.first_arg] = total_result[self.first_arg] + first_arg_result
        total_result[self.second_arg] = total_result[self.second_arg] + second_arg_result
        return total_result


class CallsNode(RelationNode):
    def __init__(self):
        super().__init__()

    def evaluate(self, pkb, with_stmt, previous_result=None):
        first_args, second_args = self.get_arguments(pkb, with_stmt, previous_result)

        for first_arg in first_args:
            first_index, first_node = list(first_arg.items())[0]
            for second_arg in second_args:
                second_index, second_node = list(second_arg.items())[0]
                if pkb.isCalling(first_index, second_node):
                    self._first_arg_result.append({first_index: first_node})
                    self._second_arg_result.append({second_index: second_node})
        return {
            self.first_arg: self._first_arg_result,
            self.second_arg: self._second_arg_result,
        }


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
        attr = MAP_ATTR_NAME_TO_NODE_ATTRIBUTE[self.attr_name]
        result = [x for x in dict_to_filter if getattr(list(x.values())[0], attr)() == self.second_arg]
        return result

    def evaluate_node(self, node):
        attr = MAP_ATTR_NAME_TO_NODE_ATTRIBUTE[self.attr_name]
        result = getattr(node, attr)() == self.second_arg
        return result


class PatternNode(Node):
    def __init__(self):
        # TODO pattern implementation
        super().__init__()

    def evaluate(self, pkb):
        pass

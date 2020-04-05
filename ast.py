import abc
from enum import Enum
from ast_interface import ASTInterface


class NodeType(Enum):
    PROCEDURE = 0,
    STMT_LST = 1,
    STMT = 2,
    ASSIGN = 3,
    VARIABLE = 4,
    INTEGER = 5,
    WHILE = 6,
    IF = 7,
    ARITHMETIC = 8,
    CALL = 9


class Node():

    def __init__(self, node_type):
        self.__type = node_type
        self.__line = None
        self.__value = None
        self.__parent = None
        self.__children = []

    def get_type(self):
        return self.__type

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    def set_line(self, line):
        self.__line = line

    def get_line(self):
        return self.__line

    def set_parent(self, parent):
        self.__parent = parent

    def get_parent(self):
        return self.__parent

    def add_child(self, node, position=None):
        if not position:
            self.__children.append(node)
        else:
            self.__children.insert(position, node)

    def get_child(self, position):
        return self.__children[position]

    def get_children(self):
        return self.__children


class AST(ASTInterface):

    def __init__(self):
        self.__root = None

    def get_child(self, parent, position):
        return parent.get_child(position)

    def get_type(self, node):
        return node.get_type()

    def get_root(self):
        return self.__root

    def is_parent(self, nodeA, nodeB):
        return nodeB.get_parent() == nodeA

    def is_parent_(self, nodeA, nodeB):
        raise NotImplementedError

    def is_parent_star(self, nodeA, nodeB):
        raise NotImplementedError

    def is_following(self, nodeA, nodeB):
        raise NotImplementedError

    def is_following_star(self, nodeA, nodeB):
        raise NotImplementedError

    def create_node(self, node_type):
        return Node(node_type)

    def set_root(self, node):
        self.__root = node

    def add_child(self, parent, child, position=None):
        parent.add_child(child, position)
        child.set_parent(parent)

    def set_parent(self, node):
        raise NotImplementedError

    def set_node_value(self, node, value):
        node.set_value(value)

    def get_node_value(self, node):
        return node.get_value()

    def get_children(self, node):
        return node.get_children()

    def set_node_line(self, node, line):
        node.set_line(line)

    def get_node_line(self, node):
        return node.get_line

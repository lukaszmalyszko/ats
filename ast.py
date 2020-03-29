import abc
from ast_interface import ASTInterface

class AST(ASTInterface):

    def get_child(self, parent, position):
        raise NotImplementedError

    def get_type(self, node):
        raise NotImplementedError

    def get_root(self):
        raise NotImplementedError

    def is_parent(self, nodeA, nodeB):
        raise NotImplementedError

    def is_parent_(self, nodeA, nodeB):
        raise NotImplementedError

    def is_parent_star(self, nodeA, nodeB):
        raise NotImplementedError

    def is_following(self, nodeA, nodeB):
        raise NotImplementedError

    def is_following_star(self, nodeA, nodeB):
        raise NotImplementedError

    def create_node(self, node_type):
        raise NotImplementedError

    def set_root(self, node):
        raise NotImplementedError

    def add_child(self, parent, child, position):
        raise NotImplementedError

    def set_parent(self, node):
        raise NotImplementedError

import abc


class ASTInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_child') and
                callable(subclass.get_child) and
                hasattr(subclass, 'get_type') and
                callable(subclass.get_type) or
                hasattr(subclass, 'get_root') and
                callable(subclass.get_root) or
                hasattr(subclass, 'is_parent') and
                callable(subclass.is_parent) or
                hasattr(subclass, 'is_parent_star') and
                callable(subclass.is_parent_star) or
                hasattr(subclass, 'is_following') and
                callable(subclass.is_following) or
                hasattr(subclass, 'is_following_star') and
                callable(subclass.is_following_star) or
                hasattr(subclass, 'create_node') and
                callable(subclass.create_node) and
                hasattr(subclass, 'set_root') and
                callable(subclass.set_root) or
                hasattr(subclass, 'add_child') and
                callable(subclass.set_root) or
                hasattr(subclass, 'set_parent') and
                callable(subclass.set_parent) or
                NotImplemented)

    @abc.abstractmethod
    def get_child(self, parent, position):
        raise NotImplementedError

    @abc.abstractmethod
    def get_type(self, node):
        raise NotImplementedError

    @abc.abstractmethod
    def get_root(self):
        raise NotImplementedError

    @abc.abstractmethod
    def is_parent(self, nodeA, nodeB):
        raise NotImplementedError

    @abc.abstractmethod
    def is_parent_(self, nodeA, nodeB):
        raise NotImplementedError

    @abc.abstractmethod
    def is_parent_star(self, nodeA, nodeB):
        raise NotImplementedError

    @abc.abstractmethod
    def is_following(self, nodeA, nodeB):
        raise NotImplementedError

    @abc.abstractmethod
    def is_following_star(self, nodeA, nodeB):
        raise NotImplementedError

    @abc.abstractmethod
    def create_node(self, node_type):
        raise NotImplementedError

    @abc.abstractmethod
    def set_root(self, node):
        raise NotImplementedError

    @abc.abstractmethod
    def add_child(self, parent, child, position):
        raise NotImplementedError

    @abc.abstractmethod
    def set_parent(self, node):
        raise NotImplementedError

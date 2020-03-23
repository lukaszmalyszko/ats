import abc


class ParserInterface(metaclass=abc.ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'create_node') and
                callable(subclass.create_node) and
                hasattr(subclass, 'set_root') and
                callable(subclass.set_root) or
                hasattr(subclass, 'add_child') and
                callable(subclass.set_root) or
                hasattr(subclass, 'set_parent') and
                callable(subclass.set_parent) or
                NotImplemented)

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

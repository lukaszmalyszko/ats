class QueryTree:
    def __init__(self):
        self._root = None

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, node):
        self._root = node

    def set_select(self, node):
        self.root.select = node

class QueryTree:
    def __init__(self):
        self.select = None
        self._root = None

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, node):
        self._root = node

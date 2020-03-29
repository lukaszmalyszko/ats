class Stmt:
    def __init__(self, name):
        self.name = name
        self.line = 'INTEGER'
        self.type = "stmt"


class While(Stmt):
    def __init__(self, name):
        super().__init__(name)


class Assign(Stmt):
    def __init__(self, name):
        super().__init__(name)


class Ref:
    def __init__(self, name):
        self.name = name
        self.type = "ref"


class Variable(Ref):
    def __init__(self, name):
        super().__init__(name)


class Constant(Ref):
    def __init__(self, name):
        super().__init__(name)
        self.value = 'INTEGER'


class ProgLine(Ref):
    def __init__(self, name):
        super().__init__(name)
        self.value = 'INTEGER'
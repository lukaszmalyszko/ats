class Declarations:
    def __init__(self):
        self.entities = {}

    def check_if_contains_variable(self, var_name):
        for var_list in self.entities.values():
            for var in var_list:
                if var_name == var.name:
                    return True
        return False

    def check_if_contains_stmt(self, stmt_name):
        # TODO
        return True

    def check_if_contains_ref(self, ref_name):
        # TODO
        return True

class Declarations:
    def __init__(self):
        self.entities = {}

    def check_if_contains_variable(self, var_name, var_type=None):
        for var_list in self.entities.values():
            for var in var_list:
                if var_name == var.name:
                    if var_type:
                        return var.type == var_type
                    return True
        return False

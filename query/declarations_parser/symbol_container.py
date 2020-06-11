class SymbolContainer:
    def __init__(self):
        self.entities = {}

    def check_if_contains_symbol(self, var_name, var_type=None):
        for var_list in self.entities.values():
            for var in var_list:
                if var_name == var.name:
                    if var_type:
                        return var.type == var_type
                    return True
        return False

    def get_symbol(self, var_name):
        for var_list in self.entities.values():
            for var in var_list:
                if var_name == var.name:
                    return var
        return False

    def get_procedure(self, proc_name):
        for proc in self.entities.get("procedure", []):
            if proc_name == proc.name:
                return proc
        return False

class ModuleError(Exception):
    """ERROR IN SRC.KARDEX"""
    pass


class InvalidCurp(ModuleError):
    """The CURP provided is not valid"""
    pass

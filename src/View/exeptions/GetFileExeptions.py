class ModuleError(Exception):
    """ERROR IN SRC.FileManager"""
    pass


class InvalidInput(ModuleError):
    """INVALID FILE INPUT"""
    pass

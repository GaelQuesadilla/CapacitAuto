class ModuleError(Exception):
    """ERROR IN SRC.LISTS"""
    pass


class InvalidOperationInLists(ModuleError):
    """The operation is not valid"""
    pass


class TryingToDeleteAnInexistentStudent(InvalidOperationInLists):
    """The operation is not valid, the student don't exist in the current list"""
    pass

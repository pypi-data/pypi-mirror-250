import endersutils
from types import ModuleType

class ModuleInstance:
    def __init__(self, module):
        if isinstance(module, ModuleType):
            self.module = module
            self.gatherModule()
        else:
            raise TypeError("Inputted value is not a module!")
    def gatherModule(self):
        return self.module

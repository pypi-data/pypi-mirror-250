class Components:
    def __init__(self) -> None:
        self.component = []

    def add_component(self, func, params):
        if callable(func):
            try:
                if type(params) == str:
                    params = (params, )
                else:
                    params = tuple(params)
                self.component.append([func, params])
            except Exception as e:
                raise e
        else:
            raise TypeError(f"Components must be a function or class method!")
    def run_component(self, idx: int):
        try:
            com = self.component
            com[idx][0](*com[idx][1])
        except IndexError:
            raise IndexError("Index is out of range!")
    def del_component(self, idx: int):
        try:
            self.component.pop(idx)
        except IndexError:
            raise IndexError("Index is out of range!")
    def list_components(self):
        com = self.component
        ret = ""
        for c in com:
            ret = ret + f"Function {c[0]}, given params {c[1]}, "
        print(ret)
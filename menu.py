from applicant import *
from interview import *


class Menu():
    menu_struct = []
    params = {}

    def __init__(self, text, parent=None, input_dict=None, module=None, method=None, filter_=None):
        self.text = text
        self.parent = next(i for i in Menu.menu_struct if i.text == parent) if parent else None
        self.input = input_dict
        self.module = module
        self.method = method
        self.filter = filter_

    @property
    def submenus(self):
        return [i for i in Menu.menu_struct if i.parent == self]

    def set_params(self):
        [Menu.params.update({v: input(k)}) for k, v in self.input.items()]
        return [Menu.params[i] for i in self.input.values()]

    def delete_params(self):
        if self.input:
            [Menu.params.pop(i) for i in self.input.values()]

    def get_params(self):
        return [Menu.params[i] if i in Menu.params.keys() else i for i in self.filter]

    def select_menu(self):
        param_list = []
        if self.filter is not None:
            param_list += self.get_params()
        if self.input:
            param_list += self.set_params()
        if self.module:
            getattr(globals().get(self.module), self.method)(*param_list)
            self.delete_params()
        else:
            self.print_menu()

    def print_menu(self):
        print("\n{0}\n{1}\n{0}".format("-"*30, self.text))
        [print("({})\t{}".format(i+1, option.text)) for i, option in enumerate(self.submenus)]
        print("(0)\tExit\n")

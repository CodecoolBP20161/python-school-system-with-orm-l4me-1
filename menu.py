from applicant import *
from interview import *
from interview_slot import *
from school import *
from mentor import *
from city import *


class Menu():
    new_id = 0
    menu_struct = []
    params = {}

    def __init__(self, text, parent=None, input_dict=None, module=None, method=None, filter_=None):
        self.id_ = Menu.new_id
        self.text = text
        self.parent = next(i for i in Menu.menu_struct if i.text == parent) if parent else None
        self.input = input_dict
        self.module = module
        self.method = method
        self.filter = filter_
        Menu.new_id += 1

    @property
    def submenus(self):
        return [i for i in Menu.menu_struct if i.parent == self]

    def set_params(self):
        for k, v in self.input.items():
            if v not in Menu.params.keys():
                Menu.params[v] = input(k)
        return [Menu.params[i] for i in self.input.values()]

    def delete_params(self):
        if self.input:
            [Menu.params.pop(i) for i in self.input.values()]

    def get_params(self):
        return [Menu.params[self.filter]] if self.filter in Menu.params.keys() else [self.filter]

    def select_menu(self):
        param_list = []
        if self.input:
            param_list = self.set_params()
        elif self.filter is not None:
            param_list = self.get_params()
        if self.module:
            getattr(globals().get(self.module), self.method)(*param_list)
            self.delete_params()
        else:
            self.print_menu()

    def print_menu(self):
        print("\n{0}\n{1}\n{0}".format("-"*30, self.text))
        for i, option in enumerate(self.submenus):
            print("({0})\t{1}".format(i+1, option.text))
        print("(0)\tExit\n")

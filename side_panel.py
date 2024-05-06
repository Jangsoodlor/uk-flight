"""The side panel and its components"""
import tkinter as tk
from tkinter import ttk

class SidePanel(tk.Frame):
    """The side panel frame"""
    def __init__(self, master=None,cnf={},**kwargs):
        super().__init__(master, cnf, **kwargs)
        self.__selectors = {}
        self.__buttons = {}
        self.__padding = {'pady':10}
        self.history_box = None

    def create_selector(self, name):
        """Creates a selector object"""
        selector = Selector(self)
        selector.label = name
        self.__selectors[name] = selector
        selector.set_state('readonly')
        selector.pack(self.__padding)

    def add_history_box(self):
        """add historybox object to the side panel"""
        self.history_box = HistoryBox(self)
        self.history_box.pack(self.__padding)

    @property
    def has_history_box(self) -> bool:
        """Returns True if there's a historybox instance inside, returns false otherwise"""
        return bool(self.history_box)

    def get_selector(self, name):
        """Get selector by name"""
        if name in self.__selectors:
            return self.__selectors[name]
        return None

    @property
    def first_selector(self):
        """returns the first selector in the side panel"""
        selector = self.__iter__()
        return next(selector)

    def get_next_selector(self, name):
        """Returns the selector that is located immediately below the one specified
        Return None if there isn't any"""
        temp_list = list(self.__selectors)
        index = temp_list.index(name)+1
        if index < len(temp_list):
            return self.__selectors[temp_list[index]]
        return None

    def disable_next_selectors(self, name):
        """Disable all selector objects located below the current one"""
        temp_list = list(self.__selectors)
        temp_list = temp_list[temp_list.index(name)+1:]
        for i in temp_list:
            self.get_selector(i).set_state('disabled')

    def get_selector_options(self):
        """Returns the options filled in the selector"""
        temp_dict = {}
        for selector in self.__selectors.values():
            temp_dict[selector.label] = selector.val
        return temp_dict

    def bind_selectors(self, func, add=None):
        """Bind all selectors to a specific function"""
        for selector in self.__selectors.values():
            selector.binder(func, add)

    def bind_selector(self, name, func, add=None):
        """Bind a specific selector"""
        self.__selectors[name].binder(func, add)

    def create_button(self, name):
        """Creates a button"""
        button = tk.Button(self, text=name)
        self.__buttons[name] = button
        button.pack(self.__padding)

    def bind_button(self, name, func, add=None):
        """bind a button to a specific function"""
        self.__buttons[name].bind('<Button>', func)

    def hide_button(self, name):
        self.__buttons[name].pack_forget()

    def get_button_state(self, name):
        """Get a state of a button"""
        return self.__buttons[name]['state']

    def set_button_state(self, name, state):
        """Set a state of a button"""
        self.__buttons[name]['state'] = state

    def hide_selector(self, name):
        """Hide a selector"""
        self.get_selector(name).pack_forget()

    def unhide_selector(self, name):
        """Unhide a selector"""
        temp_list = list(self.__selectors)
        temp_list = temp_list[temp_list.index(name)+1:]
        for i in temp_list:
            self.hide_selector(i)
        self.get_selector(name).pack(self.__padding)
        for i in temp_list:
            self.get_selector(i).pack(self.__padding)

    def __iter__(self):
        return iter(self.__selectors.values())


class HistoryBox(tk.Frame):
    """A frame that consists of a scroll bar and a listbox. It keeps track of
    what the user has selected from the selector"""
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.init_components()

    def init_components(self):
        """Initialise components"""
        self.__listbox = tk.Listbox(self)
        label = tk.Label(self, text='Selected Airlines')
        label.pack()
        scrollbar = tk.Scrollbar(self,
                                      orient='vertical',
                                      command=self.__listbox.yview)
        self.__listbox.config(yscrollcommand=scrollbar.set)
        self.__listbox.pack(side='left')
        self.__listbox_val = []
        scrollbar.pack(side='right', expand=True, fill='y')

    def __update(self):
        """Update the historybox"""
        self.__listbox['listvariable'] = tk.Variable(value=self.__listbox_val)

    @property
    def values(self):
        """Get the listbox"""
        return self.__listbox_val

    @values.setter
    def values(self, lst):
        """Set the listbox values"""
        self.__listbox_val = lst
        if not lst:
            self.__listbox.selection_clear(0, 'end')
        self.__update()

    def append(self, val):
        """Add new element to the end of the listbox"""
        self.__listbox_val.append(val)
        self.__update()

    def remove(self, val):
        """Removes an element from the listbox"""
        self.__listbox_val.remove(val)
        self.__update()

    def binder(self, func, add=None):
        """Bind the listbox. It'll inject the function with the current selection"""
        def bind_function(event):
            sel = self.__listbox.curselection()
            if sel:
                cur_sel = self.__listbox.get(sel)
                func(cur_sel)
        self.__listbox.bind('<<ListboxSelect>>', bind_function, add)

class Selector(tk.Frame):
    """An object that consists of a label and a combobox"""
    def __init__(self, master=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.__label_var = tk.StringVar()
        self.__combobox_var = tk.StringVar()
        self.init_components()

    def init_components(self):
        """init components"""
        label = tk.Label(self, textvariable=self.__label_var)
        self.__combobox = ttk.Combobox(self, textvariable=self.__combobox_var)
        pack = {'anchor':tk.CENTER}
        label.pack(pack)
        self.__combobox.pack(pack)

    def set_state(self, state):
        """Set the state of the combobox"""
        self.__combobox['state'] = state
        if state == 'disabled':
            self.__combobox_var.set('')
            self.__combobox['values'] = []

    def binder(self, func, add=None):
        """Binds the combobox"""
        def bind_function(event):
            func(self.__label_var.get())
        self.__combobox.bind('<<ComboboxSelected>>', bind_function, add)

    @property
    def label(self) -> None:
        """Return label"""
        return self.__label_var.get()

    @label.setter
    def label(self, text:str) -> None:
        """Set the label"""
        self.__label_var.set(text)

    @property
    def val(self):
        """Get the value of the combobox"""
        return self.__combobox_var.get()

    @val.setter
    def val(self, val:list) -> None:
        """Set combobox value"""
        self.__combobox['values'] = val
        self.__combobox['state'] = 'readonly'
        self.__combobox_var.set('')

    def set_selected(self, val:str):
        """Set the combobox value"""
        self.__combobox_var.set(val)

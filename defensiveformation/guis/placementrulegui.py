import tkinter as tk

from defensiveformation.guis.parametergui import ParameterGui
from defensiveformation.placementrule import PlacementRule


class PlacementRuleGui(tk.Frame):
    def __init__(self, root, placement_rule, update_callback):
        super(PlacementRuleGui, self).__init__(root)
        self.placement_rule = placement_rule
        self.update_callback = update_callback

        # Widgets for placement rule selections
        placement_rule_selection_frame = tk.Frame(self)
        placement_rule_selection_frame.grid(row=0, column=0)

        tk.Label(placement_rule_selection_frame, text='Placement Rule :').grid(row=0, column=0, sticky='E')
        placement_rule_names = PlacementRule.placement_rule_implementations.keys()
        self.placement_rule_name_value = tk.StringVar()
        self.placement_rule_name_value.set(placement_rule.name)
        self.placement_rule_om = tk.OptionMenu(placement_rule_selection_frame, self.placement_rule_name_value,
                                               *placement_rule_names,
                                               command=self.change_placement_rule)
        self.placement_rule_om.grid(row=0, column=1, sticky='WE')

        # Widgets for editing parameters
        self.parameters_frame = None
        self.change_parameters_gui()


    def change_placement_rule(self, *args):
        self.placement_rule.name = self.placement_rule_name_value.get()
        self.placement_rule.parameters = PlacementRule.placement_rule_implementations[self.placement_rule.name].get_default_parameters()
        self.change_parameters_gui()


    def change_parameters_gui(self):
        if self.parameters_frame:
            self.parameters_frame.grid_forget()
            self.parameters_frame.destroy()

        self.parameters_frame = ParameterGui(self, self.placement_rule, self.placement_rule.name, self.update_callback)
        self.parameters_frame.grid(row = 2, column = 0, sticky = 'WE')
        if self.update_callback:
            self.update_callback()
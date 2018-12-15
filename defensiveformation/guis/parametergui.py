import tkinter as tk

from defensiveformation.placementrule import PlacementRule


class ParameterGui(tk.Frame):
    def __init__(self, root, placement_rule, placement_rule_name, update_callback):
        super(ParameterGui, self).__init__(root)
        self.placement_rule = placement_rule
        self.placement_rule_name = placement_rule_name
        self.update_callback = update_callback
        parameter_list_descriptors = PlacementRule.placement_rule_implementations[placement_rule_name].parameter_descriptor

        self.parameter_widgets = []
        for i in range(len(parameter_list_descriptors)):
            descriptor = parameter_list_descriptors[i]
            parameter_name = descriptor['name']
            type = descriptor['type']
            tk.Label(self, text=parameter_name + ' :').grid(row=i, column=0, sticky='E')
            if type == 'number':
                widget = self.create_number_parameter_widget(descriptor)
                self.parameter_widgets.append({'parameter_name':parameter_name, 'type':type, 'widget':widget})
            else:
                widget, option_var = self.create_option_parameter_widget(descriptor)
                self.parameter_widgets.append({'parameter_name':parameter_name, 'type':type, 'widget':widget, 'var':option_var})
            widget.grid(row=i, column=1, sticky='EW')
        self.fill_in_starting_values()


    def create_number_parameter_widget(self, descriptor):
        min = descriptor['min']
        max = descriptor['max']
        return tk.Spinbox(self, from_ = min, to_ = max, state='readonly', command=self.update_placement_rule)


    def create_option_parameter_widget(self, descriptor):
        menu_options = descriptor['options']
        option_var = tk.StringVar()
        return tk.OptionMenu(self, option_var, *menu_options, command=self.update_placement_rule), option_var

    def fill_in_starting_values(self):
        for widget in self.parameter_widgets:
            if widget['type'] == 'number':
                widget['widget'].configure(state=tk.NORMAL)
                widget['widget'].delete(0, tk.END)
                widget['widget'].insert(0, self.placement_rule.get_parameter_value(widget['parameter_name']))
                widget['widget'].configure(state='readonly')
            else:
                widget['var'].set(self.placement_rule.get_parameter_value(widget['parameter_name']))

    def update_placement_rule(self, *args):
        for widget in self.parameter_widgets:
            if widget['type'] == 'number':
                self.placement_rule.set_parameter_value(widget['parameter_name'], int(widget['widget'].get()))
            else:
                self.placement_rule.set_parameter_value(widget['parameter_name'], widget['var'].get())
        if self.update_callback:
            self.update_callback()
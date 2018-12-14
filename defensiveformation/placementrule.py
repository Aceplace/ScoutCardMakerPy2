import tkinter as tk

from misc.exceptions import PlacementException


placement_rule_placers = {}


class PlacementRule:
    def __init__(self):
        self.name = ''
        self.parameters = []

    def place(self, offensive_formation):
        try:
            return placement_rule_placers[self.name](offensive_formation)
        except KeyError:
            raise PlacementException(f'No implementation for {self.name} placement rule')

    def get_parameter_value(self, parameter_name):
        for parameter in self.parameters:
            if parameter['name'] == parameter_name:
                return parameter['value']
        raise PlacementException(f'Couldn\'t find parameter {parameter_name}')

    def set_paremeter_value(self, parameter_name, parameter_value):
        for parameter in self.parameters:
            if parameter['name'] == parameter_name:
                parameter['value'] = parameter_value
        raise PlacementException(f'Couldn\'t update parameter {parameter_name}')


class PlacementRuleGui(tk.Frame):
    def __init__(self, root, defender, placement_rule_name, parameter_list_descriptors):
        super(PlacementRuleGui, self).__init__(root)
        self.defender = defender
        self.placement_rule_name = placement_rule_name

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
            widget.grid(row=i, column=1, sticky='W')
        self.fill_in_starting_values()


    def create_number_parameter_widget(self, descriptor):
        min = descriptor['min']
        max = descriptor['max']
        return tk.Spinbox(self, from_ = min, to_ = max, state='readonly', command=self.update_defender)


    def create_option_parameter_widget(self, descriptor):
        menu_options = descriptor['options']
        option_var = tk.StringVar()
        return tk.OptionMenu(self, option_var, *menu_options, command=self.update_defender)

    def fill_in_starting_values(self):
        for widget in self.parameter_widgets:
            if widget['type'] == 'number':
                widget['widget'].configure(state=tk.NORMAL)
                self.depth_sb.delete(0, tk.END)
                self.depth_sb.insert(0, self.defender.get_parameter_value(widget['parameter_name']))
                widget['widget'].configure(state='readonly')
            else:
                widget['var'].set(self.defender.get_parameter_value(widget['parameter_name']))

    def update_defender(self, *args):
        for widget in self.parameter_widgets:
            if widget['type'] == 'number':
                self.defender.set_parameter_value(widget['parameter_name'], int(widget['widget'].get()))
            else:
                self.defender.set_parameter_value(widget['parameter_name'], widget['var'].get())

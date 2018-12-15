import copy
import tkinter as tk

from misc.exceptions import PlacementException

class PlacementRuleImplementation:
    def __init__(self, name, default_parameters, parameter_descriptor, placer_method):
        self.name = name
        self.default_parameters = default_parameters
        self.parameter_descriptor = parameter_descriptor
        self.placer_method = placer_method

    def get_default_parameters(self):
        return copy.deepcopy(self.default_parameters)


class PlacementRule:
    placement_rule_implementations = {}
    @classmethod
    def register_placement_rule(cls, name, default_parameters, parameter_descriptor, placer_method):
        implementation = PlacementRuleImplementation(name, default_parameters, parameter_descriptor, placer_method)
        PlacementRule.placement_rule_implementations[name] = implementation

    def __init__(self, name):
        self.name = name
        try:
            self.parameters = PlacementRule.placement_rule_implementations[self.name].get_default_parameters()
        except KeyError:
            raise PlacementException(f'No implementation for {self.name} placement rule')

    def place(self, formation):
        try:
            return PlacementRule.placement_rule_implementations[self.name].placer_method(formation, self)
        except KeyError:
            raise PlacementException(f'No implementation for {self.name} placement rule')

    def get_parameter_value(self, parameter_name):
        for parameter in self.parameters:
            if parameter['name'] == parameter_name:
                return parameter['value']
        raise PlacementException(f'Couldn\'t find parameter {parameter_name}')

    def set_parameter_value(self, parameter_name, parameter_value):
        for parameter in self.parameters:
            if parameter['name'] == parameter_name:
                parameter['value'] = parameter_value
                return
        raise PlacementException(f'Couldn\'t update parameter {parameter_name}')


class PlacementRuleGui(tk.Frame):
    def __init__(self, root, placement_rule, placement_rule_name, update_callback):
        super(PlacementRuleGui, self).__init__(root)
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





if __name__=='__main__':
    from offensiveformation.formation import  Formation
    from misc.adapters import formation_to_defense_compatible_formation
    from defensiveformation.defense import Defender
    from defensiveformation.placementruledescriptors import placement_rule_descriptors
    offensive_formation = Formation()
    offensive_formation.variations['mof'].flip()
    defense_compat_formation = formation_to_defense_compatible_formation(offensive_formation, 'mof')

    defender = Defender()
    placement_rule = PlacementRule()
    placement_rule.name = 'Alignment'
    placement_rule.parameters = [
        {'name': 'Alignment', 'value': 'Seven'},
        {'name': 'Direction', 'value': 'Wk'},
        {'name': 'Strength Type', 'value': 'Receiver'},
        {'name': 'Depth', 'value': 4}
    ]
    defender.placement_rules.append(placement_rule)


    root = tk.Tk()
    PlacementRuleGui(root, placement_rule, 'Alignment', placement_rule_descriptors['Alignment']).pack(fill=tk.BOTH, expand=True)
    def place_defender():
        x, y = defender.place(defense_compat_formation)
        print(x, y)
        root.after(1000, place_defender)
    place_defender()
    root.mainloop()






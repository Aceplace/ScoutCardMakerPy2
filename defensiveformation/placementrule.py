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


if __name__=='__main__':
    from offensiveformation.formation import  Formation
    from misc.adapters import formation_to_defense_compatible_formation
    from defensiveformation.defense import Defender
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
    ParameterGui(root, placement_rule, 'Alignment', placement_rule_descriptors['Alignment']).pack(fill=tk.BOTH, expand=True)
    def place_defender():
        x, y = defender.place(defense_compat_formation)
        print(x, y)
        root.after(1000, place_defender)
    place_defender()
    root.mainloop()






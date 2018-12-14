import tkinter as tk

from defensiveformation.formationinfoutils import get_align_side, get_first_attached, get_second_attached, \
    GHOST_DISTANCE
from misc.exceptions import PlacementException


placement_rule_implementations = {}
def placement_rule_implementation(placement_rule_name):
    def inner_placement_rule_implementation(implementation):
        placement_rule_implementations[placement_rule_name] = implementation
        return implementation
    return inner_placement_rule_implementation


class PlacementRule:
    def __init__(self):
        self.name = ''
        self.parameters = []

    def place(self, formation):
        try:
            return placement_rule_implementations[self.name](formation, self)
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
    def __init__(self, root, placement_rule, placement_rule_name, parameter_list_descriptors):
        super(PlacementRuleGui, self).__init__(root)
        self.placement_rule = placement_rule
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
                self.depth_sb.insert(0, self.placement_rule.get_parameter_value(widget['parameter_name']))
                widget['widget'].configure(state='readonly')
            else:
                widget['var'].set(self.placement_rule.get_parameter_value(widget['parameter_name']))

    def update_defender(self, *args):
        for widget in self.parameter_widgets:
            if widget['type'] == 'number':
                self.placement_rule.set_parameter_value(widget['parameter_name'], int(widget['widget'].get()))
            else:
                self.placement_rule.set_parameter_value(widget['parameter_name'], widget['var'].get())




@placement_rule_implementation('Alignment')
def alignment_placement_rule(formation, placement_rule):
        alignment = placement_rule.get_parameter_value('Alignment')
        direction = placement_rule.get_parameter_value('Direction')
        strength_type = placement_rule.get_parameter_value('Strength Type')
        depth = placement_rule.get_parameter_value('Depth')
        y = depth

        align_side = get_align_side(direction, strength_type, formation)
        # modifier is affected by what side defender is on and whether they are inside or outside
        offset = -1 if 'I' in alignment else 1
        offset = offset if align_side == 'RIGHT' else offset * -1
        if alignment in ['Zero', 'Two', 'Four', 'Six', 'Eight']:
            offset = 0

        # Get alignment player
        if alignment in ['Zero', 'One']:
            align_player = formation.c
        elif alignment in ['Two_I', 'Two', 'Three']:
            align_player = formation.lg if align_side == 'LEFT' else formation.rg
        elif alignment in ['Four_I', 'Four', 'Five']:
            align_player = formation.lt if align_side == 'LEFT' else formation.rg
        elif alignment in ['Six_I', 'Six', 'Seven']:
            align_player = get_first_attached(formation, 'LT') \
                if align_side == 'left' else get_first_attached(formation, 'RT')
        elif alignment in ['Eight_I', 'Eight', 'Nine']:
            align_player = get_second_attached(formation, 'LT') \
                if align_side == 'left' else get_second_attached(formation, 'RT')

        if align_player:
            x = align_player.x + offset
        else:
            x = formation.rt.x + GHOST_DISTANCE if align_side == 'RIGHT' else formation.lt.x - GHOST_DISTANCE

        return x, y


if __name__=='__main__':
    from offensiveformation.formation import  Formation
    from defensiveformation.adapters import variation_to_defense_compatible_formation
    from defensiveformation.defense import Defender
    offensive_formation = Formation()
    defense_compat_formation = variation_to_defense_compatible_formation(offensive_formation,
                                                                         offensive_formation.variations['mof'])

    defender = Defender()
    placement_rule = PlacementRule()
    placement_rule.name = 'Alignment'
    placement_rule.parameters = [
        {'name': 'Alignment', 'value': 'Eight_I'},
        {'name': 'Direction', 'value': 'Str'},
        {'name': 'Strength Type', 'value': 'Receiver'},
        {'name': 'Depth', 'value': 4}
    ]
    defender.placement_rules.append(placement_rule)

    x, y = defender.place(defense_compat_formation)
    print(x, y)
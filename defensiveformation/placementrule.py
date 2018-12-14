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

    def set_parameter_value(self, parameter_name, parameter_value):
        for parameter in self.parameters:
            if parameter['name'] == parameter_name:
                parameter['value'] = parameter_value
                return
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
            align_player = get_first_attached(formation, 'LEFT') \
                if align_side == 'LEFT' else get_first_attached(formation, 'RIGHT')
            ghost_distance_multiplier = 1
        elif alignment in ['Eight_I', 'Eight', 'Nine']:
            align_player = get_second_attached(formation, 'LEFT') \
                if align_side == 'LEFT' else get_second_attached(formation, 'RIGHT')
            ghost_distance_multiplier = 2

        if align_player:
            x = align_player.x + offset
        else:
            x = formation.rt.x + GHOST_DISTANCE * ghost_distance_multiplier \
                if align_side == 'RIGHT' else \
                formation.lt.x - GHOST_DISTANCE * ghost_distance_multiplier

        return x, y


if __name__=='__main__':
    from offensiveformation.formation import  Formation
    from defensiveformation.adapters import variation_to_defense_compatible_formation
    from defensiveformation.defense import Defender
    from defensiveformation.placementruledescriptors import placement_rule_descriptors
    offensive_formation = Formation()
    offensive_formation.variations['mof'].flip()
    defense_compat_formation = variation_to_defense_compatible_formation(offensive_formation,
                                                                         offensive_formation.variations['mof'])

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






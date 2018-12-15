from defensiveformation.defense import BAD_PLACEMENT
from defensiveformation.formationinfoutils import get_align_side, get_receivers_inside_out, get_receivers_outside_in
from defensiveformation.placementrule import PlacementRule

apex_parameters_descriptor = [
    {
        'name':'Apex Type',
        'type':'option',
        'options':[
            'Tackle and First Receiver', 'Three and Two', 'Two and One'
        ]
    },
    {
        'name':'Direction',
        'type':'option',
        'options':[
            'Str','Wk'
        ]
    },
    {
        'name':'Strength Type',
        'type':'option',
        'options':[
            'Attached','Receiver'
        ]
    },
    {
        'name':'Depth',
        'type':'number',
        'min': 1,
        'max': 15
    }
]


apex_default_parameters = [
    {'name': 'Apex Type', 'value': 'Tackle and First Receiver'},
    {'name': 'Direction', 'value': 'Str'},
    {'name': 'Strength Type', 'value': 'Attached'},
    {'name': 'Depth', 'value': 1}
]


def apex_placer(formation, placement_rule):
    apex_type = placement_rule.get_parameter_value('Apex Type')
    direction = placement_rule.get_parameter_value('Direction')
    strength_type = placement_rule.get_parameter_value('Strength Type')
    depth = placement_rule.get_parameter_value('Depth')
    y = depth

    align_side = get_align_side(direction, strength_type, formation)
    receivers_inside_out = get_receivers_inside_out(formation, 'LEFT') if align_side == 'LEFT' else get_receivers_inside_out(formation, 'RIGHT')
    receivers_outside_in = get_receivers_outside_in(formation, 'LEFT') if align_side == 'LEFT' else get_receivers_outside_in(formation, 'RIGHT')

    if apex_type == 'Tackle and First Receiver':
        if len(receivers_inside_out) >= 1:
            x = (receivers_inside_out[0].x + formation.lt.x) // 2 if align_side == 'LEFT' else (receivers_inside_out[0].x + formation.rt.x) // 2
        else:
            x, y = BAD_PLACEMENT
    elif apex_type == 'Three and Two':
        if len(receivers_outside_in) >= 3:
            x = (receivers_outside_in[2].x + receivers_outside_in[1].x) // 2
        else:
            x, y = BAD_PLACEMENT
    else:  # apex_type == TWO_AND_ONE:
        if len(receivers_outside_in) >= 2:
            x = (receivers_outside_in[1].x + receivers_outside_in[0].x) // 2
        else:
            x, y = BAD_PLACEMENT

    return x, y

PlacementRule.register_placement_rule('Apex', apex_default_parameters, apex_parameters_descriptor, apex_placer)
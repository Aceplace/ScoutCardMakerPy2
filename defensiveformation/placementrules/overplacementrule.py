from defensiveformation.formationinfoutils import get_align_side, get_receivers_outside_across
from defensiveformation.placementrule import PlacementRule

over_parameters_descriptor = [
    {
        'name':'Over',
        'type':'option',
        'options':[
            'Number One', 'Number Two', 'Number Three', 'Number Four', 'Number Five', 'T', 'H', 'X', 'Y', 'Z', 'Q',
            'Tackle', 'Guard', 'Center'
        ]
    },
    {
        'name':'Leverage',
        'type':'option',
        'options':[
            'Inside', 'Head Up', 'Outside'
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


over_default_parameters = [
    {'name': 'Over', 'value': 'Number One'},
    {'name': 'Leverage', 'value': 'Head Up'},
    {'name': 'Direction', 'value': 'Str'},
    {'name': 'Strength Type', 'value': 'Attached'},
    {'name': 'Depth', 'value': 1}
]


def over_placer(formation, placement_rule):
    over = placement_rule.get_parameter_value('Over')
    leverage = placement_rule.get_parameter_value('Leverage')
    direction = placement_rule.get_parameter_value('Direction')
    strength_type = placement_rule.get_parameter_value('Strength Type')
    depth = placement_rule.get_parameter_value('Depth')
    y = depth

    align_side = get_align_side(direction, strength_type, formation)
    receivers_outside_across = get_receivers_outside_across(formation, 'LEFT' if align_side == 'LEFT' else 'RIGHT')
    if leverage == 'Inside':
        leverage_adjust = 1 if align_side == 'LEFT' else -1
    elif leverage == 'Outside':
        leverage_adjust = 1 if align_side == 'RIGHT' else -1
    else:
        leverage_adjust = 0

    if over == 'Number One':
        x = receivers_outside_across[0].x + leverage_adjust
    elif over == 'Number Two':
        x = receivers_outside_across[1].x + leverage_adjust
    elif over == 'Number Three':
        x = receivers_outside_across[2].x + leverage_adjust
    elif over == 'Number Four':
        x = receivers_outside_across[3].x + leverage_adjust
    elif over == 'Number Five':
        x = receivers_outside_across[4].x + leverage_adjust
    elif over == 'T':
        x = formation.t.x + leverage_adjust
    elif over == 'H':
        x = formation.h.x + leverage_adjust
    elif over == 'X':
        x = formation.x.x + leverage_adjust
    elif over == 'Y':
        x = formation.y.x + leverage_adjust
    elif over == 'Z':
        x = formation.z.x + leverage_adjust
    elif over == 'Q':
        x = formation.q.x + leverage_adjust
    elif over == 'Center':
        x = formation.c.x + leverage_adjust
    elif over == 'Tackle':
        if align_side == 'LEFT':
            x = formation.lt.x + leverage_adjust
        else:
            x = formation.rt.x + leverage_adjust
    else:
        if align_side == 'LEFT':
            x = formation.lg.x + leverage_adjust
        else:
            x = formation.rg.x + leverage_adjust

    return x, y

PlacementRule.register_placement_rule('Over', over_default_parameters, over_parameters_descriptor, over_placer)
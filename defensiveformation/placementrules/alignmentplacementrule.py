from defensiveformation.formationinfoutils import get_align_side, get_first_attached, get_second_attached, \
    GHOST_DISTANCE
from defensiveformation.placementrule import PlacementRule

alignment_parameters_descriptor = [
    {
        'name':'Alignment',
        'type':'option',
        'options':[
            'Zero','One','Two_I','Two','Three','Four_I','Four','Five','Six_I','Six','Seven','Eight_I','Eight','Nine'
        ]
    },
    {
        'name':'Direction',
        'type':'option',
        'options':[
            'Str','Wk', 'Right', 'Left'
        ]
    },
    {
        'name':'Strength Type',
        'type':'option',
        'options':[
            'Attached','Receiver','Back','Opposite of Attached','Opposite of Receiver','Opposite of Back',
            'Opposite Attached -> Opposite Receiver'
        ]
    },
    {
        'name':'Depth',
        'type':'number',
        'min': 1,
        'max': 15
    }
]

alignment_default_parameters = [
    {'name': 'Alignment', 'value': 'Zero'},
    {'name': 'Direction', 'value': 'Str'},
    {'name': 'Strength Type', 'value': 'Attached'},
    {'name': 'Depth', 'value': 1}
]

def alignment_placer(formation, placement_rule):
    alignment = placement_rule.get_parameter_value('Alignment')
    direction = placement_rule.get_parameter_value('Direction')
    strength_type = placement_rule.get_parameter_value('Strength Type')
    depth = placement_rule.get_parameter_value('Depth')
    y = depth

    if direction == 'Left':
        align_side = 'LEFT'
    elif direction == 'Right':
        align_side = 'RIGHT'
    else:
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
        align_player = formation.lt if align_side == 'LEFT' else formation.rt
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

PlacementRule.register_placement_rule('Alignment', alignment_default_parameters, alignment_parameters_descriptor, alignment_placer)
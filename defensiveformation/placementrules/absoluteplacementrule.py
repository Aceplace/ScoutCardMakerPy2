from defensiveformation.placementrule import PlacementRule

absolute_parameters_descriptor = [
    {
        'name':'Horizontal Position',
        'type':'number',
        'min': -53,
        'max': 53
    },
    {
        'name':'Depth',
        'type':'number',
        'min': 1,
        'max': 14
    }
]


absolute_default_parameters = [
    {'name': 'Horizontal Position', 'value': 0},
    {'name': 'Depth', 'value': 1}
]


def absolute_placer(formation, placement_rule):
    horizontal_position = placement_rule.get_parameter_value('Horizontal Position')
    depth = placement_rule.get_parameter_value('Depth')
    return horizontal_position, depth

PlacementRule.register_placement_rule('Absolute', absolute_default_parameters, absolute_parameters_descriptor, absolute_placer)
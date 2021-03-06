from defensiveformation.formationinfoutils import get_formation_structure, get_surface_structures, get_align_side

condition_implementations ={
    'Default': lambda formation: True,
    'Formation Structure/1x1': lambda formation: formation_structure_condition(formation, '1x1'),
    'Formation Structure/2x1': lambda formation: formation_structure_condition(formation, '2x1'),
    'Formation Structure/2x2': lambda formation: formation_structure_condition(formation, '2x2'),
    'Formation Structure/3x1': lambda formation: formation_structure_condition(formation, '3x1'),
    'Formation Structure/3x2': lambda formation: formation_structure_condition(formation, '3x2'),
    'Formation Structure/4x1': lambda formation: formation_structure_condition(formation, '4x1'),
    'Surface Structure/Rec Str/Zero Receivers': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Zero Receivers']),
    'Surface Structure/Rec Str/One Receiver': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['One Receiver']),
    'Surface Structure/Rec Str/Two Receivers': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Two Receivers']),
    'Surface Structure/Rec Str/Three Receivers': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Three Receivers']),
    'Surface Structure/Rec Str/Four Receivers': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Four Receivers']),
    'Surface Structure/Rec Str/Five Receivers': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Five Receivers']),
    'Surface Structure/Rec Str/At least One Receiver': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['At least One Receiver']),
    'Surface Structure/Rec Str/At least Two Receivers': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['At least Two Receivers']),
    'Surface Structure/Rec Str/At least Three Receivers': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['At least Three Receivers']),
    'Surface Structure/Rec Str/At least Four Receivers': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['At least Four Receivers']),
    'Surface Structure/Rec Str/Zero Attached': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Zero Attached']),
    'Surface Structure/Rec Str/One Attached': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['One Attached']),
    'Surface Structure/Rec Str/Two Attached': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Two Attached']),
    'Surface Structure/Rec Str/Three Attached': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Three Attached']),
    'Surface Structure/Rec Str/Four Attached': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Four Attached']),
    'Surface Structure/Rec Str/Five Attached': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Five Attached']),
    'Surface Structure/Rec Str/At least One Attached': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['At least One Attached']),
    'Surface Structure/Rec Str/At least Two Attached': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['At least Two Attached']),
    'Surface Structure/Rec Str/At least Three Attached': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['At least Three Attached']),
    'Surface Structure/Rec Str/At least Four Attached': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['At least Four Attached']),
    'Surface Structure/Rec Str/Nub': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Nub']),
    'Surface Structure/Rec Str/Split': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Split']),
    'Surface Structure/Rec Str/Twin': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Twin']),
    'Surface Structure/Rec Str/Pro': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Pro']),
    'Surface Structure/Rec Str/Wing': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Wing']),
    'Surface Structure/Rec Str/Trips': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Trips']),
    'Surface Structure/Rec Str/Indy': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Indy']),
    'Surface Structure/Rec Str/Indy Wing': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Indy Wing']),
    'Surface Structure/Rec Str/Tight Bunch': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Tight Bunch']),
    'Surface Structure/Rec Wk/Zero Receivers': lambda formation: surface_structure_condition(formation, 'Wk', 'Receiver', ['Zero Receivers']),
    'Surface Structure/Rec Wk/One Receiver': lambda formation: surface_structure_condition(formation, 'Wk', 'Receiver', ['One Receiver']),
    'Surface Structure/Rec Wk/Two Receivers': lambda formation: surface_structure_condition(formation, 'Wk', 'Receiver', ['Two Receivers']),
    'Surface Structure/Rec Wk/At least One Receiver': lambda formation: surface_structure_condition(formation, 'Wk', 'Receiver', ['At least One Receiver']),
    'Surface Structure/Rec Wk/Zero Attached': lambda formation: surface_structure_condition(formation, 'Wk', 'Receiver', ['Zero Attached']),
    'Surface Structure/Rec Wk/One Attached': lambda formation: surface_structure_condition(formation, 'Wk', 'Receiver', ['One Attached']),
    'Surface Structure/Rec Wk/Two Attached': lambda formation: surface_structure_condition(formation, 'Wk', 'Receiver', ['Two Attached']),
    'Surface Structure/Rec Wk/At least One Attached': lambda formation: surface_structure_condition(formation, 'Wk', 'Receiver', ['At least One Attached']),
    'Surface Structure/Rec Wk/At least Two Attached': lambda formation: surface_structure_condition(formation, 'Wk', 'Receiver', ['At least Two Attached']),
    'Surface Structure/Rec Wk/Nub': lambda formation: surface_structure_condition(formation, 'Wk', 'Receiver', ['Nub']),
    'Surface Structure/Rec Wk/Split': lambda formation: surface_structure_condition(formation, 'Wk', 'Receiver', ['Split']),
    'Surface Structure/Rec Wk/Twin': lambda formation: surface_structure_condition(formation, 'Wk', 'Receiver', ['Twin']),
    'Surface Structure/Rec Wk/Pro': lambda formation: surface_structure_condition(formation, 'Wk', 'Receiver', ['Pro']),
    'Surface Structure/Rec Wk/Wing': lambda formation: surface_structure_condition(formation, 'Wk', 'Receiver', ['Wing']),
    'Surface Structure/Rec Wk/Trips': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Trips']),
    'Surface Structure/Rec Wk/Indy': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Indy']),
    'Surface Structure/Rec Wk/Indy Wing': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Indy Wing']),
    'Surface Structure/Rec Wk/Tight Bunch': lambda formation: surface_structure_condition(formation, 'Str', 'Receiver', ['Tight Bunch']),
    'Ball Placement/MOF': lambda formation: ball_placement_condition(formation, 'MOF'),
    'Ball Placement/Hash': lambda formation: ball_placement_condition(formation, 'Hash'),
    'Ball Placement/Left Hash': lambda formation: ball_placement_condition(formation, 'Left Hash'),
    'Ball Placement/Right Hash': lambda formation: ball_placement_condition(formation, 'Right Hash'),
}

def formation_structure_condition(formation, formation_structure):
    return formation_structure == get_formation_structure(formation)

def surface_structure_condition(formation, direction, strength_type, acceptable_surface_structures):
    align_side = get_align_side(direction, strength_type, formation)
    direction_str = 'LEFT' if align_side == 'LEFT' else 'RIGHT'

    surface_structures = get_surface_structures(formation, direction_str)
    return any(structure in acceptable_surface_structures for structure in surface_structures)

def ball_placement_condition(formation, ball_placement_type):
    if ball_placement_type == 'MOF':
        return formation.hash == 'm'
    if ball_placement_type == 'Hash':
        return formation.hash != 'm'
    if ball_placement_type == 'Left Hash':
        return formation.hash == 'lt'
    if ball_placement_type == 'Right Hash':
        return formation.hash == 'rt'

def evaluate_condition(condition, formation):
    return condition_implementations[condition](formation)
ATTACH_DISTANCE = 6
GHOST_DISTANCE = 4

def get_align_side(direction, align_type, formation):
    if direction == 'LEFT' or direction == 'RIGHT':
        return direction

    if align_type == 'Attached':
        strength_direction = get_attached_strength(formation)
    elif align_type == 'Receiver':
        strength_direction = get_receiver_strength(formation)
    elif align_type == 'Back':
        strength_direction = get_back_strength(formation)
    elif align_type == 'Opposite of Attached':
        strength_direction = get_opposite_attached_strength(formation)
    elif align_type == 'Opposite of Receiver':
        strength_direction = get_opposite_receiver_strength(formation)
    elif align_type == 'Opposite Attached -> Opposite Receiver':
        strength_direction = get_opposite_attached_and_receiver_strength(formation)
    else: #Opposite of back strength
        strength_direction = get_opposite_back_strength(formation)

    if strength_direction == 'LEFT':
        if direction == 'Str':
            return 'LEFT'
        else:
            return 'RIGHT'
    else:
        if direction == 'Str':
            return 'RIGHT'
        else:
            return 'LEFT'

def get_direction_with_most_receivers(formation):
    receivers_to_left_of_lt = [player for tag, player in formation.players.items() if player.x < formation.lt.x]
    receivers_to_right_of_rt = [player for tag, player in formation.players.items() if player.x > formation.rt.x]

    if len(receivers_to_left_of_lt) > len(receivers_to_right_of_rt):
        return 'LEFT'
    if len(receivers_to_left_of_lt) < len(receivers_to_right_of_rt):
        return 'RIGHT'
    return None

def get_direction_with_most_detached_receivers(formation):
    attached_receivers_to_left = get_number_of_attached_receivers(formation, 'LEFT')
    attached_receivers_to_right = get_number_of_attached_receivers(formation, 'RIGHT')

    if attached_receivers_to_left < attached_receivers_to_right:
        return 'LEFT'
    if attached_receivers_to_left > attached_receivers_to_right:
        return 'RIGHT'
    return None

def get_direction_with_most_offset_backs(formation):
    offset_backs_to_left = get_number_of_offset_backs(formation, 'LEFT')
    offset_back_to_right = get_number_of_offset_backs(formation, 'RIGHT')

    if offset_backs_to_left > offset_back_to_right:
        return 'LEFT'
    if offset_backs_to_left < offset_back_to_right:
        return 'RIGHT'
    return None

def get_back_strength(formation, default_strength='RIGHT'):
    direction = get_direction_with_most_offset_backs(formation)
    if direction is None:
        return get_receiver_strength(formation, default_strength)
    return direction

def get_opposite_back_strength(formation, default_strength='RIGHT'):
    direction = get_direction_with_most_offset_backs(formation)
    if direction == 'LEFT':
        return 'RIGHT'
    elif direction == 'RIGHT':
        return 'LEFT'
    else:
        return get_receiver_strength(formation, default_strength)

def get_receiver_strength(formation, default_strength='RIGHT'):

    direction = get_direction_with_most_receivers(formation)
    if direction:
        return direction

    if formation.hash == 'lt':
        return 'RIGHT'
    elif formation.hash == 'rt':
        return 'LEFT'

    direction = get_direction_with_most_detached_receivers(formation)
    if direction:
        return direction

    direction = get_direction_with_most_offset_backs(formation)
    if direction:
        return direction

    return default_strength

def get_opposite_receiver_strength(formation, default_strength='RIGHT'):
    receiver_strength_direction = get_receiver_strength(formation, default_strength)

    if receiver_strength_direction == 'LEFT':
        return 'RIGHT'
    else:
        return 'LEFT'

def get_attached_strength(formation, default_strength='RIGHT'):
    attached_receivers_to_left = get_number_of_attached_receivers(formation, 'LEFT')
    attached_receivers_to_right = get_number_of_attached_receivers(formation, 'RIGHT')

    if attached_receivers_to_left > attached_receivers_to_right:
        return 'LEFT'
    if attached_receivers_to_left < attached_receivers_to_right:
        return 'RIGHT'

    return get_receiver_strength(formation, default_strength)

def get_opposite_attached_strength(formation, default_strength='RIGHT'):
    attached_receivers_to_left = get_number_of_attached_receivers(formation, 'LEFT')
    attached_receivers_to_right = get_number_of_attached_receivers(formation, 'RIGHT')

    if attached_receivers_to_left > attached_receivers_to_right:
        return 'RIGHT'
    if attached_receivers_to_left < attached_receivers_to_right:
        return 'LEFT'

    return get_receiver_strength(formation, default_strength)

def get_opposite_attached_and_receiver_strength(formation, default_strength='RIGHT'):
    attached_receivers_to_left = get_number_of_attached_receivers(formation, 'LEFT')
    attached_receivers_to_right = get_number_of_attached_receivers(formation, 'RIGHT')

    if attached_receivers_to_left > attached_receivers_to_right:
        return 'RIGHT'
    if attached_receivers_to_left < attached_receivers_to_right:
        return 'LEFT'

    return get_opposite_receiver_strength(formation, default_strength)

def get_number_of_receivers(formation, direction):
    if direction == 'LEFT':
        return len([player for tag, player in formation.players.items() if player.x < formation.lt.x])
    elif direction == 'RIGHT':
        return len([player for tag, player in formation.players.items() if player.x > formation.rt.x])

def get_number_of_attached_receivers(formation, direction):
    number_of_attached_receivers = 0

    if direction == 'LEFT':
        sorted_receivers_outside_tackle = list(sorted([player for tag, player in formation.players.items() if player.x < formation.lt.x], key=lambda player: player.x))
        sorted_receivers_outside_tackle.reverse()
        outside_most_attached_player = formation.lt
    else:
        sorted_receivers_outside_tackle = list(sorted([player for tag, player in formation.players.items() if player.x > formation.rt.x], key=lambda player: player.x))
        outside_most_attached_player = formation.rt

    for player in sorted_receivers_outside_tackle:
        if abs(player.x - outside_most_attached_player.x) <= ATTACH_DISTANCE:
            number_of_attached_receivers += 1
            outside_most_attached_player = player

    return number_of_attached_receivers


def get_number_of_offset_backs(formation, direction):
    number_of_attached_receivers = 0
    if direction == 'LEFT':
        return len([player for tag, player in formation.players.items() if player.x >= formation.lt.x and player.x < formation.c.x])
    else:
        return len([player for tag, player in formation.players.items() if player.x <= formation.rt.x and player.x > formation.c.x])


def get_first_attached(formation, direction):
    if direction == 'LEFT':
        sorted_receivers_outside_tackle = list(
            sorted([player for tag, player in formation.players.items() if player.x < formation.lt.x],
                   key=lambda player: player.x))
        sorted_receivers_outside_tackle.reverse()
        outside_most_attached_player = formation.lt
    else:
        sorted_receivers_outside_tackle = list(
            sorted([player for tag, player in formation.players.items() if player.x > formation.rt.x],
                   key=lambda player: player.x))
        outside_most_attached_player = formation.rt

    for player in sorted_receivers_outside_tackle:
        if abs(player.x - outside_most_attached_player.x) <= ATTACH_DISTANCE:
            return player

    return None


def get_second_attached(formation, direction):
    number_of_attached_receivers = 0

    if direction == 'LEFT':
        sorted_receivers_outside_tackle = list(
            sorted([player for tag, player in formation.players.items() if player.x < formation.lt.x],
                   key=lambda player: player.x))
        sorted_receivers_outside_tackle.reverse()
        outside_most_attached_player = formation.lt
    else:
        sorted_receivers_outside_tackle = list(
            sorted([player for tag, player in formation.players.items() if player.x > formation.rt.x],
                   key=lambda player: player.x))
        outside_most_attached_player = formation.rt

    for player in sorted_receivers_outside_tackle:
        if abs(player.x - outside_most_attached_player.x) <= ATTACH_DISTANCE:
            number_of_attached_receivers += 1
            if (number_of_attached_receivers == 2):
                return player
            outside_most_attached_player = player

    return None


def get_receivers_outside_across(formation, direction):
    if formation.q.x != 0:
        receivers = [player for tag, player in formation.players.items() if tag in ['t', 'h', 'x', 'y', 'z', 'q']]
    else:
        receivers = [player for tag, player in formation.players.items() if tag in ['t', 'h', 'x', 'y', 'z']]

    if direction == 'LEFT':
        receivers.sort(key = lambda player: (player.x, player.y))
    else:
        receivers.sort(key = lambda player: (-1 * player.x, player.y))

    return receivers

def get_receivers_outside_in(formation, direction):
    if formation.q.x != 0:
        receivers = [player for tag, player in formation.players.items() if tag in ['t', 'h', 'x', 'y', 'z', 'q']]
    else:
        receivers = [player for tag, player in formation.players.items() if tag in ['t', 'h', 'x', 'y', 'z']]

    if direction == 'LEFT':
        receivers.sort(key = lambda player: (player.x, player.y))
        filtered_receivers = [receiver for receiver in receivers if receiver.x < formation.lt.x]
    else:
        receivers.sort(key = lambda player: (-1 * player.x, player.y))
        filtered_receivers = [receiver for receiver in receivers if receiver.x > formation.rt.x]

    return filtered_receivers

def get_receivers_inside_out(formation, direction):
    if formation.q.x != 0:
        receivers = [player for tag, player in formation.players.items() if tag in ['t', 'h', 'x', 'y', 'z', 'q']]
    else:
        receivers = [player for tag, player in formation.players.items() if tag in ['t', 'h', 'x', 'y', 'z']]

    if direction == 'LEFT':
        receivers.sort(key = lambda player: (-1 * player.x, player.y))
        filtered_receivers = [receiver for receiver in receivers if receiver.x < formation.lt.x]
    else:
        receivers.sort(key = lambda player: (player.x, player.y))
        filtered_receivers = [receiver for receiver in receivers if receiver.x > formation.rt.x]

    return filtered_receivers


def get_formation_structure(formation):
    receivers_to_left = get_number_of_receivers(formation, 'LEFT')
    receivers_to_right = get_number_of_receivers(formation, 'RIGHT')
    if receivers_to_left == 1 and receivers_to_right == 1:
        return '1x1'
    if (receivers_to_left == 1 and receivers_to_right == 2) or (receivers_to_left == 2 and receivers_to_right == 1):
        return '2x1'
    if receivers_to_left == 2 and receivers_to_right == 2:
        return '2x2'
    if (receivers_to_left == 3 and receivers_to_right == 1) or (receivers_to_left == 1 and receivers_to_right == 3):
        return '3x1'
    if (receivers_to_left == 3 and receivers_to_right == 2) or (receivers_to_left == 2 and receivers_to_right == 3):
        return '3x2'
    return '4x1'



def get_surface_structures(formation, direction):
    surface_structure = []
    number_of_receivers = get_number_of_receivers(formation, direction)
    number_of_attached_receivers = get_number_of_attached_receivers(formation, direction)
    if number_of_receivers == 0:
        surface_structure.append('Zero Receivers')
    elif number_of_receivers == 1:
        surface_structure.append('One Receiver')
        surface_structure.append('At least One Receiver')
    elif number_of_receivers == 2:
        surface_structure.append('Two Receivers')
        surface_structure.append('At least One Receiver')
        surface_structure.append('At least Two Receivers')
    elif number_of_receivers == 3:
        surface_structure.append('Three Receivers')
        surface_structure.append('At least One Receiver')
        surface_structure.append('At least Two Receivers')
        surface_structure.append('At least Three Receivers')
    elif number_of_receivers == 4:
        surface_structure.append('Four Receivers')
        surface_structure.append('At least One Receiver')
        surface_structure.append('At least Two Receivers')
        surface_structure.append('At least Three Receivers')
        surface_structure.append('At least Four Receivers')
    elif number_of_receivers == 5:
        surface_structure.append('Five Receivers')
        surface_structure.append('At least One Receiver')
        surface_structure.append('At least Two Receivers')
        surface_structure.append('At least Three Receivers')
        surface_structure.append('At least Four Receivers')

    if number_of_attached_receivers == 0:
        surface_structure.append('Zero Attached')
    elif number_of_attached_receivers == 1:
        surface_structure.append('One Attached')
        surface_structure.append('At least One Attached')
    elif number_of_attached_receivers == 2:
        surface_structure.append('Two Attached')
        surface_structure.append('At least One Attached')
        surface_structure.append('At least Two Attached')
    elif number_of_attached_receivers == 3:
        surface_structure.append('Three Attached')
        surface_structure.append('At least One Attached')
        surface_structure.append('At least Two Attached')
        surface_structure.append('At least Three Attached')
    elif number_of_attached_receivers == 4:
        surface_structure.append('Four Attached')
        surface_structure.append('At least One Attached')
        surface_structure.append('At least Two Attached')
        surface_structure.append('At least Three Attached')
        surface_structure.append('At least Four Attached')
    elif number_of_attached_receivers == 5:
        surface_structure.append('Five Attached')
        surface_structure.append('At least One Attached')
        surface_structure.append('At least Two Attached')
        surface_structure.append('At least Three Attached')
        surface_structure.append('At least Four Attached')


    if number_of_receivers == 1 and number_of_attached_receivers == 1:
        surface_structure.append('Nub')
    if number_of_receivers == 1 and number_of_attached_receivers == 0:
        surface_structure.append('Split')

    if number_of_receivers == 2 and number_of_attached_receivers == 0:
        surface_structure.append('Twin')
    if number_of_receivers == 2 and number_of_attached_receivers == 1:
        surface_structure.append('Pro')
    if number_of_receivers == 2 and number_of_attached_receivers == 2:
        surface_structure.append('Wing')

    if number_of_receivers == 3 and number_of_attached_receivers == 0:
        surface_structure.append('Trips')
    if number_of_receivers == 3 and number_of_attached_receivers == 1:
        surface_structure.append('Indy')
    if number_of_receivers == 3 and number_of_attached_receivers == 2:
        surface_structure.append('Indy Wing')
    if number_of_receivers == 3 and number_of_attached_receivers == 3:
        surface_structure.append('Tight Bunch')

    return surface_structure


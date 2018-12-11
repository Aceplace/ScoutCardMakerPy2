import copy

class Player:
    def __init__(self, tag, label, type, eligible):
        self.tag = tag
        self.label = label
        self.type = type
        self.eligible = eligible

class Formation:
    def __init__(self):
        self.players = {}
        self.players['lt'] = Player('lt', 'LT', 'line', False)
        self.players['lg'] = Player('lg', 'LG', 'line', False)
        self.players['c'] = Player('c', 'C', 'line', False)
        self.players['rg'] = Player('rg', 'RG', 'line', False)
        self.players['rt'] = Player('rt', 'RT', 'line', False)
        self.players['t'] = Player('t', 'T', 'backfield', True)
        self.players['h'] = Player('h', 'H', 'backfield', True)
        self.players['x'] = Player('x', 'X', 'backfield', True)
        self.players['y'] = Player('y', 'Y', 'attached', True)
        self.players['z'] = Player('z', 'Z', 'attached', True)
        self.players['q'] = Player('q', 'Q', 'attached', False)
        self.affected_player_tags = []
        self.variations = {
            'mof': get_default_variation('mof'),
            'field': get_default_variation('field'),
            'boundary': get_default_variation('boundary')
        }



class FormationVariation:
    def __init__(self):
        self.players = {}

    def copy_variation_from_variation(self, variation):
        self.players = copy.deepcopy(variation.players)

    def override_player_positions(self, override_variation, override_tags):
        for tag in override_tags:
            self.players[tag].x = override_variation.players[tag].x
            self.players[tag].y = override_variation.players[tag].y

    def flip(self):
        for player in self.players.values():
            player.x *= -1
        self.players['lt'].x, self.players['rt'].x = self.players['rt'].x, self.players['lt'].x
        self.players['lg'].x, self.players['rg'].x = self.players['rg'].x, self.players['lg'].x

def get_default_variation(type):
    variation = FormationVariation()
    if type == 'mof':
        variation.players['lt'] = {'x': -8, 'y': 1}
        variation.players['lg'] = {'x': -4, 'y': 1}
        variation.players['c'] = {'x': 0, 'y': 1}
        variation.players['rg'] = {'x': 4, 'y': 1}
        variation.players['rt'] = {'x': 8, 'y': 1}
        variation.players['t'] = {'x': 0, 'y': 7}
        variation.players['h'] = {'x': 0, 'y': 5}
        variation.players['x'] = {'x': -35, 'y': 1}
        variation.players['y'] = {'x': 12, 'y': 1}
        variation.players['z'] = {'x': 35, 'y': 2}
        variation.players['q'] = {'x': 0, 'y': 2}
    elif type == 'field':
        variation.players['lt'] = {'x': -26, 'y': 1}
        variation.players['lg'] = {'x': -22, 'y': 1}
        variation.players['c'] = {'x': -18, 'y': 1}
        variation.players['rg'] = {'x': -14, 'y': 1}
        variation.players['rt'] = {'x': -10, 'y': 1}
        variation.players['t'] = {'x': -18, 'y': 7}
        variation.players['h'] = {'x': -18, 'y': 5}
        variation.players['x'] = {'x': -35, 'y': 1}
        variation.players['y'] = {'x': -6, 'y': 1}
        variation.players['z'] = {'x': 35, 'y': 2}
        variation.players['q'] = {'x': -18, 'y': 2}
    else:
        variation.players['lt'] = {'x': 10, 'y': 1}
        variation.players['lg'] = {'x': 14, 'y': 1}
        variation.players['c'] = {'x': 18, 'y': 1}
        variation.players['rg'] = {'x': 22, 'y': 1}
        variation.players['rt'] = {'x': 26, 'y': 1}
        variation.players['t'] = {'x': 18, 'y': 7}
        variation.players['h'] = {'x': 18, 'y': 5}
        variation.players['x'] = {'x': -18, 'y': 1}
        variation.players['y'] = {'x': 30, 'y': 1}
        variation.players['z'] = {'x': 18, 'y': 2}
        variation.players['q'] = {'x': 18, 'y': 2}
    return variation
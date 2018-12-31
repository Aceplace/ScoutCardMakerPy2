from collections import namedtuple
from collections.__init__ import namedtuple


def formation_to_visualizer(formation, variation_name):
    formation_variation = formation.variations[variation_name]
    VisualizerPlayer = namedtuple('VisualizerPlayer', 'tag label x y')
    visualizer_players = []
    for player in formation.players.values():
        tag = player.tag
        label = player.label
        x = formation_variation.players[tag]['x']
        y = formation_variation.players[tag]['y']
        visualizer_players.append(VisualizerPlayer(tag=tag, label=label, x=x, y=y))

    VisualizerFormation = namedtuple('VisualizerFormation', 'players')
    visualizer_formation = VisualizerFormation(players=visualizer_players)

    return visualizer_formation

def variation_to_visualizer(variation):
    VisualizerPlayer = namedtuple('VisualizerPlayer', 'tag label x y')
    visualizer_players = []
    for tag, player in variation.players.items():
        label = tag.upper() if len(tag) == 1 else tag[1].upper()
        x = player['x']
        y = player['y']
        visualizer_players.append(VisualizerPlayer(tag=tag, label=label, x=x, y=y))

    VisualizerFormation = namedtuple('VisualizerFormation', 'players')
    visualizer_formation = VisualizerFormation(players=visualizer_players)

    return visualizer_formation

def variation_to_powerpoint(variation):
    PPPlayer = namedtuple('PPPlayer', 'label x y')
    pp_players = {}
    for tag, player in variation.players.items():
        label = tag.upper()
        x = player['x']
        y = player['y']
        pp_players[label] = PPPlayer(label=label, x=x, y=y)

    PPFormation = namedtuple('PPFormation', 'players')
    pp_formation = PPFormation(players=pp_players)

    return pp_formation


def variation_to_defense_compatible_formation(variation):
    FormationPlayer = namedtuple('FormationPlayer', 'tag label x y')
    formation_players = {}
    for tag, player in variation.players.items():
        label = tag.upper() if len(tag) == 1 else tag[1].upper()
        x = player['x']
        y = player['y']
        formation_players[tag] = FormationPlayer(tag=tag, label=label, x=x, y=y)

    DefenseCompatibleFormation = namedtuple('DefenseCompatibleFormation', 'players t, h, x, y, z, q lt lg c rt rg hash')
    defensive_compatible_formation = DefenseCompatibleFormation(
        players=formation_players,
        t=formation_players['t'],
        h=formation_players['h'],
        x=formation_players['x'],
        y=formation_players['y'],
        z=formation_players['z'],
        q=formation_players['q'],
        lt=formation_players['lt'],
        lg=formation_players['lg'],
        c=formation_players['c'],
        rg=formation_players['rg'],
        rt=formation_players['rt'],
        hash=variation.hash
    )

    return defensive_compatible_formation

def placed_defense_to_visualizer(placed_defenders, affected_defender_tags):
    VisualizerPlayer = namedtuple('VisualizerDefender', 'tag label x y')
    visualizer_players = []
    for tag, label, x, y in placed_defenders:
        visualizer_players.append(VisualizerPlayer(tag=tag, label=label, x=x, y=y))

    VisualizerFormation = namedtuple('VisualizerDefense', 'players affected_defender_tags')
    visualizer_formation = VisualizerFormation(players=visualizer_players, affected_defender_tags=affected_defender_tags)

    return visualizer_formation
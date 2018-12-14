from collections import namedtuple

def variation_to_defense_compatible_formation(formation, variation):
    FormationPlayer = namedtuple('FormationPlayer', 'tag label x y')
    formation_players = {}
    for player in formation.players.values():
        tag = player.tag
        label = player.label
        x = variation.players[tag]['x']
        y = variation.players[tag]['y']
        formation_players[tag] = FormationPlayer(tag=tag, label=label, x=x, y=y)

    DefenseCompatibleFormation = namedtuple('DefenseCompatibleFormation', 'players q lt lg c rt rg')
    defensive_compatible_formation = DefenseCompatibleFormation(
        players=formation_players,
        q=formation_players['q'],
        lt=formation_players['lt'],
        lg=formation_players['lg'],
        c=formation_players['c'],
        rg=formation_players['rg'],
        rt=formation_players['rt']
    )

    return defensive_compatible_formation
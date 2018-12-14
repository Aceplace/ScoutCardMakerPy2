from collections import namedtuple

def variation_to_visualizer(formation, variation):
    VisualizerPlayer = namedtuple('VisualizerPlayer', 'tag label x y')
    visualizer_players = []
    for player in formation.players.values():
        tag = player.tag
        label = player.label
        x = variation.players[tag]['x']
        y = variation.players[tag]['y']
        visualizer_players.append(VisualizerPlayer(tag=tag, label=label, x=x, y=y))

    VisualizerFormation = namedtuple('VisualizerFormation', 'players')
    visualizer_formation = VisualizerFormation(players=visualizer_players)

    return visualizer_formation

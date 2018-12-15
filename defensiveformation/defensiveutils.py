from defensiveformation.defense import Defense
from defensiveformation.placementrule import PlacementRule


def get_default_defense():
    defense = Defense()
    for defender in defense.defenders.values():
        defender.placement_rules.append(PlacementRule('Alignment'))
    return defense
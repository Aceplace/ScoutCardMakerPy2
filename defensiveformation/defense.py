import copy

from defensiveformation.conditions import evaluate_condition
from defensiveformation.placementruleutils import get_default_placement_rule

BAD_PLACEMENT = (55, 15)

class ConditionSet:
    def __init__(self):
        self.conditions = ['Default']
        self.connectors = ['first']

    def condition_set_satisfied(self, formation):
        one_condition_unsatisfied = False
        for condition, connector in zip(self.conditions, self.connectors):
            if connector == 'or' and not one_condition_unsatisfied:
                return True
            elif connector == 'or':
                one_condition_unsatisfied = False

            if not evaluate_condition(condition, formation):
                one_condition_unsatisfied = True
        return not one_condition_unsatisfied

    def __repr__(self):
        return f'ConditionSet{{Conditions: {self.conditions}, Connectors: {self.connectors}}}'


class Defender:
    def __init__(self, tag, label):
        self.tag = tag
        self.label = label
        self.condition_sets = [ConditionSet()]
        self.placement_rules = [get_default_placement_rule()]

    def place(self, formation):
        found_suitable_condition = False
        for condition_set, placement_rule in zip(self.condition_sets, self.placement_rules):
            if condition_set.condition_set_satisfied(formation):
                x, y = placement_rule.place(formation)
                found_suitable_condition = True
                break
        if not found_suitable_condition:
            x , y = BAD_PLACEMENT

        return x, y

class Defense:
    def __init__(self):
        self.defenders = {}
        self.defenders['t'] = Defender('t', 'T')
        self.defenders['n'] = Defender('n', 'N')
        self.defenders['p'] = Defender('p', 'P')
        self.defenders['a'] = Defender('a', 'A')
        self.defenders['w'] = Defender('w', 'W')
        self.defenders['m'] = Defender('m', 'M')
        self.defenders['b'] = Defender('b', 'B')
        self.defenders['s'] = Defender('s', 'S')
        self.defenders['f'] = Defender('f', 'F')
        self.defenders['c'] = Defender('c', 'C')
        self.defenders['q'] = Defender('q', 'Q')
        self.affected_defender_tags = []

    def override_defenders(self, override_defense):
        for tag in override_defense.affected_defender_tags:
            self.defenders[tag] = copy.deepcopy(override_defense.defenders[tag])
            if tag not in self.affected_defender_tags:
                self.affected_defender_tags.append(tag)

    def get_placed_defenders(self, formation):
        placed_defenders = []
        for tag, defender in self.defenders.items():
            x, y = defender.place(formation)
            placed_defenders.append((defender.tag, defender.label, x, y))
        return placed_defenders

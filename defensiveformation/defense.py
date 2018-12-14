BAD_PLACEMENT = (55, 15)

def evaluate_condition(condition, formation):
    return True

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


class Defender:
    def __init__(self):
        self.condition_sets = []
        self.placement_rules = []

    def place(self, formation):
        """found_suitable_condition = False
        for condition_set, placement_rule in zip(self.condition_set, self.placement_rules):
            if condition_set.condition_set_satisfied(formation):
                x, y = self.placement_rule.place(formation)
                found_suitable_condition = True
                break
        if not found_suitable_condition:
            x , y = BAD_PLACEMENT"""

        x, y = self.placement_rules[0].place(formation)
        return x, y

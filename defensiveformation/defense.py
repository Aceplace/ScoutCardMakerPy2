BAD_PLACEMENT = (55, 15)

def evaluate_condition(condition, offensive_formation):
    return True

class ConditionSet:
    def __init__(self):
        self.conditions = ['Default']
        self.connectors = ['first']

    def condition_set_satisfied(self, offensive_formation):
        one_condition_unsatisfied = False
        for condition, connector in zip(self.conditions, self.connectors):
            if connector == 'or' and not one_condition_unsatisfied:
                return True
            elif connector == 'or':
                one_condition_unsatisfied = False

            if not evaluate_condition(condition, offensive_formation):
                one_condition_unsatisfied = True
        return not one_condition_unsatisfied


class Defender:
    def __init__(self):
        self.condition_sets = []
        self.placement_rules = []

    def place(self, offensive_formation):
        found_suitable_condition = False
        for condition_set, placement_rule in zip(self.condition_set, self.placement_rules):
            if condition_set.condition_set_satisfied(offensive_formation):
                x, y = self.placement_rule.place(offensive_formation)
                found_suitable_condition = True
                break
        if not found_suitable_condition:
            x , y = BAD_PLACEMENT

        return x, y

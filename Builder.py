from collections import Counter
from Components import *
from CompatibilityDatabase import *


class Builder:
    def __init__(self, clientID: str, database):
        self.clientID = clientID
        self.conflicts = []
        self._database = database
        self.suggestions = dict()

    def build(self, component_set) -> bool:
        """
        :param component_set: a set of client provided components
        :return: True if build succeeds, False otherwise
        """
        self.validate_entry(component_set)
        self.conflicts.clear()
        self.suggestions.clear()

        self.check_conflict(component_set)
        if len(self.conflicts) != 0:
            self.suggestions = self.suggest_resolve()
            return False
        return True

    def validate_entry(self, component_set: set):
        """
        ensures exactly one primary component in the car, each exists in inventory
        :param component_set: set of components
        :return: True if valid, False otherwise
        """
        counter = Counter()
        for comp in component_set:
            if comp not in self._database.inventory:
                raise KeyError("Component: " + str(comp.name) + " not in inventory")
            if comp.comp_type != Component_Type.Extra:
                counter[comp.comp_type] += 1
        assert (val == 1 for val in counter.values())

    def check_conflict(self, component_set: set):
        """
        checks conflicts among components
        :param component_set: set of current components
        :return: None
        """
        for comp1 in component_set:
            for comp2 in component_set:
                if comp1 != comp2:
                    if not self._database.compatibility(comp1, comp2):
                        self.conflicts.append((comp1, comp2))

    def suggest_resolve(self):
        # TODO: Needs a lot of successful client build data to train
        # Open ended, can be a Neural network or k-means clustering
        # to suggest other similar items instead of conflicting items

        # For now, I will just suggest components that are not
        # conflicting with one of the components in the setup
        # for every conflict

        """
        returns potential resolves for conflicts
        :return: dictionary of potential resolves for each component
        """

        suggestions = dict()
        for conflict in self.conflicts:
            suggestion_ids = set()
            if conflict[0] in self._database.dependencies:
                suggestion_ids = self._database.dependencies[conflict[0]]
            need_type = conflict[1].comp_type
            suggests = [self._database.component_from_id(comp_id) for comp_id in suggestion_ids]
            suggests = [comp for comp in suggests if comp.comp_type == need_type]
            if conflict[0] not in suggestions:
                suggestions[conflict[0]] = set()
            suggestions[conflict[0]].union(suggests)

        return suggestions

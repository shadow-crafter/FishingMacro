

"""
States:

1-Evaluating mode. Decides if enough time has passed for player to eat.
    ->if it is time to eat, enter 5.
    ->if it is not time to eat, casts rod and enters 2.
2-Searching mode. Looking for exclamation point
    -> if detected, enter 3
    -> if alarm threshold passes, enters 4
3-Fishing mode. clicks on repeat while checking for "caught" text
    -> if "caught" text detected, return to 1
    -> if enough time passes, enters 4
4-Stuck mode. Plays alarm sound when entered if enabled, and re-equips rod before returning to 1.
5-Eating mode. makes the player eat based on pre-defined button, then returns to 1.

"""


class MacroState:
    def execute(self):
        raise NotImplementedError("This method is ment to be overridden!")

class EvaluatingMode(MacroState):
    def execute(self):
        pass

class SearchingMode(MacroState):
    def execute(self):
        pass

class FishingMode(MacroState):
    def execute(self):
        pass

class StuckMode(MacroState):
    def execute(self):
        pass

class EatingMode(MacroState):
    def execute(self):
        pass

def run_macro():
    current_macro_state = EvaluatingMode()

    while current_macro_state is not None:
        current_macro_state = current_macro_state.execute()
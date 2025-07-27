from pynput.keyboard import Listener
import random
from src.processing import *
from src.settings import *
from src.util import play_alarm_sound
import threading
import time

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

class Macro:
    sound_file_path = "sounds/alert.mp3"

    center_x, center_y = (-1, -1) #used for mouse click location
    current_macro_state = None

    def on_press(self, key):
        try:
            if key.char == pause_keybind:
                if self.current_macro_state != self.PausedMode:
                    current_macro_state = self.PausedMode()
                    print("Macro has been paused.")
                else:
                    current_macro_state = self.StuckMode() #automatically assume stuck, so restart
                    print("Macro has been unpaused.")
            if key.char == stop_keybind:
                print("Stopping macro...")
                current_macro_state = self.ExitMode()
        except AttributeError:
            pass #do nothing, only catches exception if it's a special key like f1 or shift

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

    class PausedMode(MacroState):
        def execute(self):
            pass

    class ExitMode(MacroState):
        def execute(self):
            return None

    def listen_for_input(self):
        with Listener(on_press=self.on_press) as listener:
            listener.join()

    def run_macro(self):
        self.current_macro_state = self.EvaluatingMode()

        listener_thread = threading.Thread(target=self.listen_for_input)
        listener_thread.daemon = True
        listener_thread.start()

        while self.current_macro_state is not None:
            self.current_macro_state = self.current_macro_state.execute()

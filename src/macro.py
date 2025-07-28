import keyboard
from pynput.keyboard import Controller, Listener
import random
from src.cli import CLI
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
6-Paused mode. Must be exited manually.
7.Exit mode. Ends macro.
"""

sound_file_path = "sounds/alert.mp3"
exclamation_wait_time = 3
fishing_wait_time = 15 #how long program will try to fish for
key_press_delay = 0.01
key_press_interval = 0.25
click_interval = 0.01

class Macro:
    current_macro_state = None
    pyn_keyboard = Controller()
    cli = CLI

    last_clicked_time = time.time()
    eating_timer = time.time()
    fish_caught = 0

    def __init__(self):
        self.cli = CLI(self)

    @classmethod
    def key_checks(cls):
        if keyboard.is_pressed(pause_keybind):
            if not isinstance(cls.current_macro_state, cls.PausedMode):
                cls.current_macro_state = cls.PausedMode()
                cls.cli.extra_info.append("Macro has been paused.")
            else:
                cls.current_macro_state = cls.StuckMode()
            time.sleep(0.2) #db
            return cls.current_macro_state
        elif keyboard.is_pressed(stop_keybind):
            cls.cli.extra_info.append("Stopping macro...")
            cls.current_macro_state = cls.ExitMode()
            time.sleep(0.2) #db
            return cls.current_macro_state
    
    @classmethod
    def click(cls):
        center_x, center_y = get_game_window_center(get_game_window())
        try:
            pyautogui.click(center_x, center_y)
            cls.last_clicked_time = time.time()
            time.sleep(click_interval + (random.random() / 1000)) #variance for bot detection
        except pyautogui.FailSafeException:
            cls.cli.extra_info.append("Macro failed to click!")

    @classmethod
    def press_key(cls, key):
        try:
            cls.pyn_keyboard.press(key)
            time.sleep(key_press_delay)
            cls.pyn_keyboard.release(key)
            time.sleep(key_press_interval)
        except Exception as err:
            cls.cli.extra_info.append("Could not press key!!: " + str(err))
    
    @classmethod
    def safety_return_checks(cls):
        if isinstance(cls.current_macro_state, Macro.ExitMode): #checks while in loops
            return cls.current_macro_state
        elif isinstance(cls.current_macro_state, Macro.PausedMode):
            return cls.current_macro_state
        return None
    
    class MacroState:
        state_info = "should be overridden"
        def execute(self):
            raise NotImplementedError("This method is ment to be overridden!")

    class EvaluatingMode(MacroState):
        state_info = "evaluating..."
        def execute(self):
            if time.time() - Macro.eating_timer >= eat_time:
                return Macro.EatingMode()
            else:
                time.sleep(0.3) #delay after caught
                Macro.click()
                return Macro.SearchingMode()

    class SearchingMode(MacroState):
        state_info = "searching for an exclamation point..."
        def execute(self):
            while time.time() - Macro.last_clicked_time < alarm_time:
                check = Macro.key_checks()
                if check:
                    return check

                if detect_exclamation(contour_area_threshold) and time.time() - Macro.last_clicked_time >= exclamation_wait_time: #sometimes exclamation lingers
                    return Macro.FishingMode()

            return Macro.StuckMode()

    class FishingMode(MacroState):
        state_info = "fishing!!"
        def execute(self):
            fishing_timer = time.time()
            while time.time() - fishing_timer < fishing_wait_time:
                check = Macro.key_checks()
                if check:
                    return check
                
                if found_text_in_image():
                    Macro.cli.extra_info.append("Caught a fish!")
                    Macro.fish_caught += 1
                    return Macro.EvaluatingMode()
                
                Macro.click()
            
            return Macro.StuckMode()

    class StuckMode(MacroState):
        state_info = "stuck, attempting to get unstuck..."
        def execute(self):
            if play_alarm:
                play_alarm_sound(sound_file_path)
            
            Macro.press_key(rod_equip_keybind)
            Macro.press_key(rod_equip_keybind)
            
            return Macro.EvaluatingMode()

    class EatingMode(MacroState):
        state_info = "eating!!"
        def execute(self):
            Macro.press_key(food_equip_keybind)
            Macro.click()
            time.sleep(0.3) #give extra time for eating to process
            Macro.press_key(rod_equip_keybind)

            Macro.eating_timer = time.time()
            return Macro.EvaluatingMode()

    class PausedMode(MacroState):
        state_info = "paused..."
        def execute(self):
            Macro.cli.extra_info.append("Macro is paused.")
            time.sleep(0.1)
            return self

    class ExitMode(MacroState):
        state_info = "exiting..."
        def execute(self):
            return None

    def run_macro(self):
        self.cli.extra_info.append("Starting macro...")
        
        self.current_macro_state = self.EvaluatingMode()

        while self.current_macro_state is not None:

            macro_state = self.current_macro_state.execute()
            check = self.key_checks()
            #print("before: ", macro_state)
            #print("current: ", self.current_macro_state)
            #print("check: ", check)
            if check:
                if isinstance(check, Macro.ExitMode):
                    self.current_macro_state = None
                else:
                    self.current_macro_state = check
            else:
                self.current_macro_state = macro_state
        
        cv2.destroyAllWindows()
        self.cli.extra_info.append("Macro ended successfully.")

import os
import playsound #needs 1.2.2 version to install for me
import pyautogui
from pynput.keyboard import Listener
import pygetwindow as gw
import random
import time

sound_file_path = "alert.mp3"
window_check_title = "roblox"

target_colors = [(236, 32, 34), (248, 80, 80)] #red of fishing alert exclamation point
click_interval = 0.01
alarm_threshold = 25 #how long before macro tries to get unstuck / play alarm

center_x, center_y = 0, 0 #used for mouse click location

stop_macro = False

def on_press(key):
    global stop_macro

    try:
        if key.char == '`':
            print("Stopping macro...")
            stop_macro = True

            return False #end listener thread
    except AttributeError:
        pass #do nothing, only catches exception if it's a special key like f1 or shift

def play_alarm_sound(file_path):
    if not os.path.exists(file_path):
        print(f"The file at '{file_path}' does not exist.")
        return
    
    try:
        playsound.playsound(file_path)
    except Exception as e:
        print(f"An error occured while trying to play a sound: {e}")

def exclamation_detected(target_color, tolerance=35, check_length=350) -> bool:
    global center_x, center_y

    try:
        windows = gw.getAllWindows()
        
        game_window: gw.Window = None
        for window in windows:
            if window_check_title.lower() in window.title.lower(): #check for window with keyword, in this case the one for the game
                game_window = window
                break
        
        if not game_window:
            print(f"No window with '{window_check_title}' in the title was found.")
            return
        
        if not game_window.isActive:
            try:
                game_window.activate()
                time.sleep(0.4) #allow time to focus window
            except Exception as e:
                print(f"Could not activate the window '{game_window.title}': {e}")
                print("The program will attempt to screenshot anyway--it will likely not work as intended.")

        center_x, center_y = game_window.left + game_window.right // 2, game_window.top + game_window.height // 2

        left = min(game_window.left, center_x - (check_length // 2)) #subtract half check length since square is centered
        top = min(game_window.top, center_y - (check_length // 2))

        check_w, check_h = check_length

        if left + check_length > game_window.left + game_window.width: #ensure it doesn't check out of game window
            check_w = (game_window.left + game_window.width) - left
        if top + check_length < game_window.top + game_window.height:
            check_h = (game_window.top + game_window.height) - top

        screenshot = pyautogui.screenshot(region=(left, top, check_w, check_h))

        for x in range(screenshot.width):
            for y in range(screenshot.height):
                pixel_color = screenshot.getpixel((x, y))

                #check if pixel color is close enough to the target
                if abs(pixel_color[0] - target_color[0]) <= tolerance and abs(pixel_color[1] - target_color[1] <= tolerance) and abs(pixel_color[2] - target_color[2] <= tolerance):
                    print(f"Found the color {pixel_color} at ({left + x}, {top + y})")
                    return True
        
        return False
    except Exception as e:
        print(f"An error has occured: {e}")

def macro():
    global center_x, center_y

    last_clicked_time = 0

    print("Macro is starting...")
    time.sleep(2) #delay starting macro
    print("Macro started!")
    while not stop_macro:
        if exclamation_detected(target_color=target_colors[0]) or exclamation_detected(target_color=target_colors[1]):
            pyautogui.click(center_x, center_y)
            last_clicked_time = time.time()
            time.sleep(click_interval + ((random.random() * 2) / 100)) #variance for bot detection
        elif time.time() - last_clicked_time >= alarm_threshold: #attempt to get unstuck if no clicks in a while
            pyautogui.click(center_x, center_y)
            #play_alarm_sound(sound_file_path) #optionally play alarm sound too
            last_clicked_time = time.time()

if __name__ == "__main__":
    with Listener(on_press=on_press) as listener: #creates thread to run on_press alongside macro
        macro()

        listener.join() #joins thread to make sure program closes correctly
    print("Macro ended successfully.")

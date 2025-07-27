from pynput.keyboard import Listener
import random
from src.processing import *
from src.util import play_alarm_sound
import time

sound_file_path = "alert.mp3"

click_interval = 0.01
alarm_threshold = 45 #how long before macro tries to get unstuck / play alarm

center_x, center_y = (-1, -1) #used for mouse click location

play_alarm = True

stop_macro = False
pause_macro = False

def on_press(key):
    global stop_macro
    global pause_macro

    try:
        if key.char == '=':
            pause_macro = not pause_macro
            if pause_macro == True:
                print("Macro has been paused.")
            else:
                print("Macro has been unpaused.")
        if key.char == '`':
            print("Stopping macro...")
            stop_macro = True
            return False
    except AttributeError:
        pass #do nothing, only catches exception if it's a special key like f1 or shift

def macro():
    global center_x, center_y

    last_clicked_time = time.time()

    print("Macro is starting...")
    time.sleep(2) #delay starting macro
    print("Macro started!")
    while not stop_macro:
        if pause_macro:
            continue
        if detect_exclamation(contour_area_threshold) and time.time() - last_clicked_time >= 1:
            while not found_text_in_image(text_checks) and not stop_macro:
                pyautogui.click(center_x, center_y)
                last_clicked_time = time.time()
                time.sleep(click_interval + (random.random() / 1000)) #variance for bot detection
            time.sleep(0.5) #delay after caught
            pyautogui.click(center_x, center_y)
            last_clicked_time = time.time()
        elif time.time() - last_clicked_time >= alarm_threshold and center_x != -1 and center_y != -1: #attempt to get unstuck if no clicks in a while
            pyautogui.click(center_x, center_y)
            if play_alarm:
                play_alarm_sound(sound_file_path) #optionally play alarm sound too
            last_clicked_time = time.time()

if __name__ == "__main__":
    with Listener(on_press=on_press) as listener: #creates thread to run on_press alongside macro
        macro()

        listener.join() #joins thread to make sure program closes correctly
    cv2.destroyAllWindows()
    print("Macro ended successfully.")

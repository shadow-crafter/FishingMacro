import cv2
import numpy as np
import os
import playsound
import pyautogui
from pynput.keyboard import Listener
import pygetwindow as gw
import pytesseract as tess
import random
import re
import time

sound_file_path = "alert.mp3"
window_check_title = "Roblox"
ignore_list = ["Firefox", "Chrome", "Opera", "Brave", "Edge", "Vivaldi"] #if user has roblox open in a browser, it can confuse the game window detection

text_checks = ("Caught", "Cought") #the "a" gets detected wrong commonly
#target_colors = {"lower": np.array([236, 32, 34]), "higher": np.array([248, 80, 80])}
target_colors1 = {"lower": np.array([0, 100, 100]), "higher": np.array([10, 255, 255])}
target_colors2 = {"lower": np.array([160, 100, 100]), "higher": np.array([180, 255, 255])}
click_interval = 0.01
alarm_threshold = 45 #how long before macro tries to get unstuck / play alarm

center_x, center_y = (-1, -1) #used for mouse click location

play_alarm = True
debug_windows = True # shows windows of where the program is looking for an image or text. Only reccomended for testing since this decreases performance

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

def play_alarm_sound(file_path: str) -> None:
    if not os.path.exists(file_path):
        print(f"The file at '{file_path}' does not exist.")
        return
    
    try:
        playsound.playsound(file_path)
    except Exception as e:
        print(f"An error occured while trying to play a sound: {e}")

def ignore_list_check(title: str) -> bool:
    for word in ignore_list:
        if word.lower() in title:
            return False
    return True

def get_window_screenshot(check_length):
    global center_x, center_y

    windows = gw.getAllWindows()
        
    game_window = None
    for window in windows:
        if window_check_title.lower() in window.title.lower() and ignore_list_check(window.title.lower()): #check for window with keyword & not browser
            game_window = window
            break
    
    if not game_window:
        print(f"No window with '{window_check_title}' in the title was found.")
        center_x, center_y = (-1, -1)
        return None
        
    if not game_window.isActive:
        try:
            game_window.activate()
            time.sleep(0.4) #allow time to focus window
        except Exception as e:
            print(f"Could not activate the window '{game_window.title}': {e}")
            print("The program will attempt to screenshot anyway--it will likely not work as intended.")

    if check_length != 0:
        center_x, center_y = game_window.left + game_window.width // 2, game_window.top + game_window.height // 2

        left = max(game_window.left, center_x - (check_length // 2)) #subtract half check length since square is centered
        top = max(game_window.top, center_y - (check_length // 2))

        check_w, check_h = (check_length, check_length)

        if left + check_length > game_window.left + game_window.width: #ensure it doesn't check out of game window
            check_w = (game_window.left + game_window.width) - left
        if top + check_length > game_window.top + game_window.height:
            check_h = (game_window.top + game_window.height) - top

        screenshot = pyautogui.screenshot(region=(left, top, check_w, check_h))
    else:
        screenshot = pyautogui.screenshot(region=(game_window.left, game_window.top, game_window.width, game_window.height))
    
    screenshot.save("screenshot_region.png")

    return screenshot

def detect_exclamation(contour_check_area: int) -> bool:
    try:
        screenshot = get_window_screenshot(500)
        if screenshot is None:
            return False
        
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV) #convert to hsv
        screenshot = cv2.resize(screenshot, (0, 0), fx=0.5, fy=0.5)

        mask1 = cv2.inRange(screenshot, target_colors1["lower"], target_colors1["higher"])
        mask2 = cv2.inRange(screenshot, target_colors2["lower"], target_colors2["higher"])
        mask = cv2.bitwise_or(mask1, mask2)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        found = False
        for contour in contours:
            area = cv2.contourArea(contour)
            print(area)
            if area > contour_check_area:
                x, y, w, h = cv2.boundingRect(contour)

                cv2.rectangle(screenshot, (x,y), (x+w, y+h), (0, 0, 255), 2)

                found = True
        
        if debug_windows:
            cv2.imshow("Detected Exclamation Point", screenshot)
            cv2.waitKey(1)

        return found
    except Exception as e:
        print(f"An error has occured: {e}")
        return False

def found_text_in_image(text_checks: tuple) -> bool:
    try:
        screenshot = get_window_screenshot(0)
        if screenshot is None:
            return False
        
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        h, w = screenshot.shape
        screenshot = screenshot[h // 2:h, round(w // 1.5):w]
        
        if debug_windows:
            cv2.imshow("Detected Text Area", screenshot)
            cv2.waitKey(1)

        extracted_text = tess.image_to_string(screenshot)
        extracted_text = extracted_text.lower()
        extracted_text = re.sub(r'[^a-zA-Z0-9]', ' ', extracted_text) # remove special characters that sometimes artifact
        print(f"Extracted text: {extracted_text.strip()}")

        for text_check in text_checks:
            if text_check.lower() in extracted_text:
                return True
        
        return False
    except Exception as e:
        print(f"An error has occured: {e}")
        return False

def macro():
    global center_x, center_y

    last_clicked_time = time.time()

    print("Macro is starting...")
    time.sleep(2) #delay starting macro
    print("Macro started!")
    while not stop_macro:
        if pause_macro:
            continue
        if detect_exclamation(70) and time.time() - last_clicked_time >= 1:
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

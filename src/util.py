import os
import playsound

def play_alarm_sound(file_path: str) -> None:
    if not os.path.exists(file_path):
        print(f"The file at '{file_path}' does not exist.")
        return
    
    try:
        playsound.playsound(file_path)
    except Exception as e:
        print(f"An error occured while trying to play a sound: {e}")

def ignore_list_check(title: str, ignore_list: list[str]) -> bool:
    for word in ignore_list:
        if word.lower() in title:
            return False
    return True

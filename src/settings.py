import configparser

config = configparser.ConfigParser()
config.read('config.ini')

window_check_title = config.get("Settings", "window_title")
ignore_list = config.get("Settings", "ignore_list").split(',')

contour_area_threshold = int(config.get("Settings", "contour_area_threshold"))

debug_windows = bool(config.get("Settings", "debug_windows"))
play_alarm = bool(config.get("Settings", "play_alarm"))

alarm_time = int(config.get("Settings", "alarm_time"))
eat_time = int(config.get("Settings", "eat_time")) * 60 #convert to minutes

pause_keybind = config.get("Settings", "pause_keybind")
stop_keybind = config.get("Settings", "stop_keybind")
rod_equip_keybind = config.get("Settings", "rod_equip_keybind")
food_equip_keybind = config.get("Settings", "food_equip_keybind")

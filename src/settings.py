import configparser

config = configparser.ConfigParser()
config.read('config.ini')

window_check_title = config.get("Settings", "window_title")
ignore_list = config.get("Settings", "ignore_list").split(',')
contour_area_threshold = int(config.get("Settings", "contour_area_threshold"))
debug_windows = bool(config.get("Settings", "debug_windows"))
play_alarm = bool(config.get("Settings", "play_alarm"))
click_interval = float(config.get("Settings", "click_interval"))
alarm_threshold = int(config.get("Settings", "alarm_threshold"))

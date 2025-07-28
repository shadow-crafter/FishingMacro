# Fishing Macro

Made for use in the game [Arcane Odyssey](https://www.roblox.com/games/3272915504/Arcane-Odyssey-Early-Access) on Roblox. This program allows you to automatically catch fish in game.

It works by first detecting red pixels in the center of the screen (as in looking for the red exclamation point you see when you catch a fish), triggering a sequence of clicking while checking for the "caught" message, and then repeating.

The program also has a timer for automatic eating to make the process easier.

*Please note that using this tool AFK is against the rules of the game and you may be banned.*

## Installation

### From Source Code
Installing the program is straightforward.

- Firstly, <b>make sure that you have</b> [Python](https://www.python.org/downloads/) and Pip installed and working.

- Next, extract the project and place it somewhere <b>that makes sense to you.</b>

Once these steps are done, you need to install the dependencies.
To do this, follow these steps:

- Open your terminal, and navigate to the project.
- (Optional, but reccommended) create a venv environment first in the project with this command: `python -m venv venv`
- If you decide to use venv, activate it with `./venv/scripts/activate`
- Now install the dependencies by running `pip install -r requirements.txt`

After following these steps, you should be able to run the program by running `python main.py`

If you would like an .exe file you can use to run the program, follow these steps:
- Run the command `pip install pyinstaller`
- Run the command `pyinstaller --onefile main.py`

### From Release

TBA

## Usage

### Setup
To use the program, open Arcane Odyssey on Roblox and start the program.

It is reccomended to calibrate it first to make sure it works well on your device.

To do this, head into the <i>config.ini</i> file in this project, and change `debug_windows` to <b>true</b>. This will create popups when the program takes screenshots, allowing you to adjust paramaters accordingly. It is reccomended to test this with the game window in a windowed state to make it easier to compare (since the program auto focuses the game window).

The paramater `contour_area_threshold` is the minimum number of red pixles the program must detect in a contour to begin fishing. If the program is too sensitive on your device, lower this value--if it isn't sensitive enough, increase it.

The paramater `check_size` is how big the screenshot the program takes is in the center of the screen. This will likely need to be adjusted based on your screen size or game window size.

To make sure the program properly detects the exclamation point when fishing, position your camera in a way to make it as <b>clear as possible.</b> Make sure you are also in a well-lit area with as little background noise as possible. Additionally, remove any red accessories or items equipped from your character.

(example image here)

It is also reccomended to disable trade & message notifications just in case they pile up and the program is unable to see the caught popup.

Finally, configure the `pause_kebind`, `stop_keybind`, `rod_equip_keybind`, and the `food_equip_keybind` to your liking. Keep in mind that the pause & stop buttons must be held rather than pressed to work, and that the pause button is a bit finicky at the moment.

The `rod_equip_keybind` should be the number the program needs to press to equip your fishing rod in your inventory, and the `food_equip_keybind` be the number for your food of choice.

### Fishing time!

Once everything is configured and working, you can turn the `debug_windows` back to false if you would like.

If you would like an alarm to play when the program is stuck, set `play_alarm` to true. Generally the program is able to fix itself, but you may want an alarm to remind you to check. You can change the sound by replacing the <i>alert.mp3</i> file in the <i>sounds/</i> directory in the project.

When your ready, just start the program and leave it running and watch it catch the fish! When you are done, hold the stop key until the program ends.

If you would like to multitask while it fishes for you, you can put the game window in a windowed state or split-screen it with another window. Just make sure that the game window is focused. Additionally, keep in mind that the program will need to click and press keys for you in the game window.

<b><u>DO NOT USE THIS PROGRAM AFK. IT IS AGAINST THE RULES AND YOU MAY BE BANNED.</b></u>


## Contributing

Contributions to the project are welcome.
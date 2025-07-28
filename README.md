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
- Run the command `python -m pyinstaller --onefile main.py`

### From Release

TBA

## Usage

## Contributing

Contributions to the project are welcome.
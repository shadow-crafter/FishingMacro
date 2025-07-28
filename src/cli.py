from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import threading
import time

class CLI:
    macro = None
    extra_info = []

    def __init__(self, mac) -> None:
        self.macro = mac
        cli_thread = threading.Thread(target=self.update_cli)
        cli_thread.daemon = True
        cli_thread.start()

    def update_cli(self):
        while True:
            if self.macro:
                console = Console()

                if self.macro.current_macro_state != None:
                    state_info = self.macro.current_macro_state.state_info
                else:
                    state_info = "exiting..."

                title = Text("Fishing Macro", style="bold cyan")
                panel = Panel(
                    f"fish caught this session: 0 total fish caught: 0\n"
                    f"The macro is currently {state_info}\n",
                    title=title,
                    border_style="bright_blue"
                )

                console.clear()
                console.print(panel) 
                for line in self.extra_info:
                    console.print(line)

                time.sleep(0.5)

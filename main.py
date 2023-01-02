from pyTwistyScrambler import scrambler333
from time import monotonic
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Static, Header, Footer, Button
from textual.containers import Container
from textual.events import Key

class ScrambleDisplay(Static):
    """A widget to display the scramble"""

    scramble = scrambler333.get_WCA_scramble()

    def new_scramble(self) -> None:
        self.scramble = scrambler333.get_WCA_scramble()
        self.update(self.scramble)


class Timer(Static):
    """A widget to display time"""

    start_time = reactive(monotonic)
    time = reactive(0.0)
    total = reactive(0.0)
    started = reactive(False)

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.update_timer = self.set_interval(1 / 60, self.update_time, pause=True)


    def update_time(self) -> None:
        """Method to update the time to the current time."""
        self.time = self.total + (monotonic() - self.start_time)

    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")

    def start(self) -> None:
        """Method to start (or resume) time updating."""
        self.start_time = monotonic()
        self.update_timer.reset()
        self.update_timer.resume()
        self.started = True

    def stop(self):
        """Method to stop the time display updating."""
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total
        self.started = False

    def reset(self):
        """Method to reset the time display to zero."""
        self.total = 0
        self.time = 0

class Scramble(Static):
    scramble = reactive("[b]" + scrambler333.get_WCA_scramble() + "[/b]")

    def compose(self) -> ComposeResult:
        yield ScrambleDisplay(self.scramble)
        yield Timer("00:00")



class SpeedCubeTimer(App):

    CSS_PATH = "styles.css"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]


    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        yield Scramble()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def key_space(self) -> None:
        """Event handler called when a button is pressed."""
        time_display = self.query_one(Timer)
        # time_display.start_stop()
        if time_display.started :
            time_display.stop()
            scramble_display = self.query_one(ScrambleDisplay)
            scramble_display.new_scramble()
        else:
            time_display.reset()
            time_display.start()


if __name__ == "__main__":
    app = SpeedCubeTimer()
    app.run()
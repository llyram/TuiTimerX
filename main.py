from pyTwistyScrambler import scrambler333
from time import monotonic
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Static, Header, Footer, Button, DataTable
from textual.containers import Container
from textual.events import Key
from textual import log

import csv


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
        yield DataTable(id="time-record")

        yield Scramble()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        with open('solves.csv') as csv_file:
            rows = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in rows:
                if(line_count == 0):
                    table.add_columns(*row)
                else:
                    table.add_row(*row)
                line_count+=1


    

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def key_space(self) -> None:
        """Event handler called when a button is pressed."""
        time_display = self.query_one(Timer)
        # """ time_display.start_stop()"""
        if time_display.started :
            """ Stop the timer and update the scramble"""
            time_display.stop()
            scramble_display = self.query_one(ScrambleDisplay)
            scramble_display.new_scramble()

            def ao5(table, time):
                if(table.row_count < 4):
                    return 0
                times = table.get_column_at(1)
                times = [float(x) for x in times]
                return "%.2f" % (sum(sorted(times[-4:])[1:-1], time) / 3)
            
            def ao12(table, time):
                if(table.row_count < 11):
                    return 0
                times = table.get_column_at(1)
                times = [float(x) for x in times]
                return "%.2f" % (sum(times[-11:], time) / 12)

            """ update the data table"""
            table = self.query_one(DataTable)
            data_row = [
                table.row_count+1,
                "%.2f" % time_display.time, 
                ao5(table, time_display.time),
                ao12(table, time_display.time),
            ]

            

            table.add_row(*data_row)
            # table.refresh_row(table.row_count)

            with open('solves.csv', mode='a') as solves_file:
                solves = csv.writer(solves_file, delimiter=',')
                solves.writerow(data_row)

        else:
            time_display.reset()
            time_display.start()


if __name__ == "__main__":
    app = SpeedCubeTimer()
    app.run()
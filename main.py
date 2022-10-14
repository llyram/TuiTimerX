from textual.widgets import Placeholder
from rich.panel import Panel

from textual.app import App
from textual.reactive import Reactive
from textual.widget import Widget

from scramble import genScramble

class Scramble(Widget):

    mouse_over = Reactive(False)
    scramble = Reactive("[b]" + genScramble() + "[/b]")

    def render(self) -> Panel:
        return Panel(self.scramble, border_style="green" if self.mouse_over else "blue", title="Scramble")

    def on_enter(self) -> None:
        self.mouse_over = True

    def on_leave(self) -> None:
        self.mouse_over = False

class Solves(Widget):

    mouse_over = Reactive(False)

    def render(self) -> Panel:
        return Panel("Previous solves table", border_style="green" if self.mouse_over else "blue", title="Solves")

    def on_enter(self) -> None:
        self.mouse_over = True

    def on_leave(self) -> None:
        self.mouse_over = False

class Timer(Widget):

    mouse_over = Reactive(False)

    def render(self) -> Panel:
        return Panel("Timer", border_style="green" if self.mouse_over else "blue", title="Timer")

    def on_enter(self) -> None:
        self.mouse_over = True

    def on_leave(self) -> None:
        self.mouse_over = False

class HoverApp(App):
    """Demonstrates custom widgets"""

    async def on_mount(self) -> None:
        await self.view.dock(Solves(), edge="left", size=40)
        await self.view.dock(Scramble(), Timer(), edge="top")
        # hovers = (Hover() for _ in range(10))
        # await self.view.dock(*hovers, edge="top")/


HoverApp.run(log="textual.log")
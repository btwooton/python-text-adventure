from __future__ import annotations

from tcod import libtcodpy

from collections.abc import Callable
from typing import Protocol

import attrs
import tcod.console
import tcod.event
from tcod.event import KeySym

import game.state_tools
import game.constants as constants
from game.state import Pop, StateResult, State
from game.ui_helpers import get_colored_string, strip_coloration


class MenuItem(Protocol):

    __slots__ = ()

    def on_event(self, event: tcod.event.Event) -> StateResult:
        """Handle events passed to the menu item."""

    def on_draw(self, console: tcod.console.Console, x: int, y: int, highlight: bool) -> None:
        """Draw this item at the given position."""

    def get_rendered_width(self) -> int:
        """Return the width in columns of this menu item."""

    def get_rendered_height(self) -> int:
        """Return the height in rows of this menu item."""


@attrs.define()
class SelectItem(MenuItem):
    """Clickable menu item."""

    label: str
    callback: Callable[[], StateResult]

    def on_event(self, event: tcod.event.Event) -> StateResult:
        """Handle events selecting this item."""
        match event:
            case tcod.event.KeyDown(sym=sym) if sym in {KeySym.RETURN, KeySym.RETURN2, KeySym.KP_ENTER}:
                print(f"callback triggered on item {self.label}")
                return self.callback()
            case tcod.event.MouseButtonUp(button=tcod.event.MouseButton.LEFT):
                return self.callback()
            case _:
                return None

    def on_draw(self, console: tcod.console.Console, x: int, y: int, highlight: bool) -> None:
        """Render this item"""
        console.print(
            x, y, self.label, 
            fg=(255, 255, 255), 
            bg=(64, 64, 64) if highlight else (0, 0, 0)
        )

    def get_rendered_width(self) -> int:
        return len(self.label)

    def get_rendered_height(self) -> int:
        return 1


@attrs.define()
class ListMenu(MenuItem):

    items: tuple[MenuItem, ...]
    selected: int | None = 0
    origin_x: int = attrs.field(default=0, init=False)
    origin_y: int = attrs.field(default=0, init=False)

    def on_event(self, event: tcod.event.Event) -> StateResult:
        match event:
            case tcod.event.KeyDown(sym=sym) if sym in constants.DIRECTION_KEYS:
                dx, dy = constants.DIRECTION_KEYS[sym]
                if dx != 0 or dy == 0:
                    return self.activate_selected(event)
                if self.selected is not None:
                    self.selected += dy
                    self.selected %= len(self.items)
                else:
                    self.selected = 0 if dy == 1 else len(self.items) - 1
                return None
            case tcod.event.MouseMotion(position=(_, y)):
                y -= self.origin_y
                self.selected = int(y) if 0 <= y < len(self.items) else None
                return None
            case _:
                return self.activate_selected(event)

    def activate_selected(self, event: tcod.event.Event) -> StateResult:
        if self.selected is not None:
            return self.items[self.selected].on_event(event)
        return None

    def on_draw(self, console: tcod.console.Console, x: int, y: int, highlight: bool) -> None:
        """Render the menu."""
        self.origin_x, self.origin_y = x, y
        for i, item in enumerate(self.items):
            item.on_draw(console, x=x, y=y + i, highlight=i == self.selected)

    def get_rendered_width(self) -> int:
        return max(item.get_rendered_width() for item in self.items)

    def get_rendered_height(self) -> int:
        return len(self.items)


@attrs.define()
class MenuPanel(MenuItem):

    padding_horizontal: int
    padding_vertical: int
    child_item: MenuItem

    def on_draw(self, console: tcod.console.Console, x: int, y: int, highlight: bool) -> None:
        # draw the frame
        console.draw_frame(
            x, y, 
            width=self.get_rendered_width(), 
            height=self.get_rendered_height(),
            decoration=constants.FRAME_DECORATION,
            fg=(255, 255, 255)
        )

        # draw the inner child
        self.child_item.on_draw(console, x=x + self.padding_horizontal, y=y + self.padding_vertical, highlight=highlight)

    def on_event(self, event: tcod.event.Event) -> StateResult:
        return self.child_item.on_event(event)

    def get_rendered_height(self):
        return self.child_item.get_rendered_height() + 2 * self.padding_vertical

    def get_rendered_width(self):
        return self.child_item.get_rendered_width() + 2 * self.padding_horizontal


@attrs.define()
class WrappedText(MenuItem):

    max_width: int
    text: str

    def on_draw(self, console: tcod.console.Console, x: int, y: int, highlight: bool) -> None:
        console.print(
            x, y, 
            text=self.text,
            width=self.max_width,
            alignment=libtcodpy.LEFT
        )

    def on_event(self, event: tcod.event.Event) -> StateResult:
        return None

    def get_rendered_width(self):
        return self.max_width

    def get_rendered_height(self):
        return tcod.console.get_height_rect(self.max_width, self.text)


@attrs.define()
class FixedSizeTextArea(MenuItem):

    max_width: int
    max_height: int
    paragraphs: list[str] = attrs.field(factory=list)

    def on_draw(self, console: tcod.console.Console, x: int, y: int, highlight: bool) -> None:
        # display only the last 5 paragraphs
        paragraphs_to_display = self.paragraphs[-10:]
        # now highlight the last paragraph and gray out the others
        text = "\n\n".join([
            get_colored_string(p, 255, 255, 255) 
            if i == len(paragraphs_to_display) - 1 
            else get_colored_string(strip_coloration(p), 64, 64, 64)
            for i, p in enumerate(paragraphs_to_display)
        ])
        console.print(
            x, y,
            text=text,
            width=self.max_width,
            height=self.max_height,
            fg=(255, 255, 255)
        )

    def on_event(self, event: tcod.event.Event) -> StateResult:
        return None

    def get_rendered_width(self) -> int:
        return self.max_width

    def get_rendered_height(self) -> int:
        return self.max_height



@attrs.define()
class MenuState(State):
    """Puts a tree of MenuItems on the stack. The only menu piece that knows states exist"""

    root_item: MenuItem
    x: int = 0
    y: int = 0

    def on_event(self, event: tcod.event.Event) -> StateResult:
        match event:
            case tcod.event.Quit():
                raise SystemExit
            case tcod.event.KeyDown(sym=KeySym.ESCAPE) | tcod.event.MouseButtonUp(
                button=tcod.event.MouseButton.RIGHT
            ):
                return self.on_cancel()
            case _:
                return self.root_item.on_event(event)

    def on_cancel(self) -> StateResult:
        return Pop()

    def on_draw(self, console: tcod.console.Console) -> None:
        # now draw and dim whatever sits beneath this menu
        game.state_tools.draw_previous_state(self, console)
        # now draw the whole menu tree from its root
        self.root_item.on_draw(console, x=self.x, y=self.y, highlight=False)


        

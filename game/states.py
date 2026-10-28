from __future__ import annotations

import tcod.console
import tcod.event
from tcod.event import KeySym
from collections.abc import Callable

import g
import game.menus
from game.state import State, Reset, Push, StateResult


def enter_room(room_id: str) -> StateResult:
    g.player.current_room_id = room_id
    return Reset(InGame(room_id))

def make_move_callback(room_id: str) -> Callable[[], StateResult]:
    def enter_chosen_room() -> StateResult:
        return enter_room(room_id)

    return enter_chosen_room

def get_item(item_id: str, room_id: str) -> StateResult:
    room = g.world.get_room(room_id)
    item = room.items.pop(item_id, None)
    if item is not None:
        g.player.inventory[item_id] = item

    return Reset(InGame(room_id))


def make_get_callback(item_id: str, room_id: str) -> Callable[[], StateResult]:
    def get_chosen_item() -> StateResult:
        return get_item(item_id, room_id)

    return get_chosen_item



class InGame(State):
    """Primary in-game state."""

    def __init__(self, room_id: str) -> None:
        print(f"Initializing InGame with room_id {room_id}")
        room = g.world.get_room(room_id)
        description = room.get_description()
        exits = room.exits
        self.intro_blurb = game.menus.MenuPanel(child_item=game.menus.WrappedText(
            max_width=30,
            text=description
        ), padding_horizontal=2, padding_vertical=2)   

        self.player_choices = game.menus.MenuPanel(child_item=game.menus.ListMenu(
            items=[
                game.menus.SelectItem(
                    f"Go {exit_direction}: {g.world.get_room(room_id).name}",
                    callback=make_move_callback(room_id)
                )
                for exit_direction, room_id in exits.items()
            ] + [
                game.menus.SelectItem(
                    f"Get {item.name}",
                    callback=make_get_callback(item_id, room_id)
                )
                    for item_id, item in room.items.items()
            ],
            selected=0
        ), padding_horizontal=2, padding_vertical=2)

    def on_event(self, event: tcod.event.Event) -> StateResult:
        match event:
            case tcod.event.Quit():
                raise SystemExit
            case tcod.event.KeyDown(sym=KeySym.ESCAPE):
                return Push(PaneledMainMenu())
            case _:
                return self.player_choices.on_event(event)

    def on_draw(self, console: tcod.console.Console) -> None:
        self.intro_blurb.on_draw(console, 4, 4, False)

        self.player_choices.on_draw(console, 4, 4 + self.intro_blurb.get_rendered_height() + 4, False)

    def update_rendered_description(self, description: str) -> None:
        self.intro_blurb.child_item.text = description

type MenuCallback = Callable[[], StateResult]

def build_main_menu_items(new_game: MenuCallback, continue_game: MenuCallback, quit_game: MenuCallback) -> tuple[game.menus.MenuItem, ...]:
    continue_items = [game.menus.SelectItem("Continue", continue_game)] if hasattr(g, "world") else []
    return (
        *continue_items,
        game.menus.SelectItem("New game", new_game),
        game.menus.SelectItem("Quit", quit_game),
    )


class PaneledMainMenu(game.menus.MenuState):

    __slots__ = ()

    def __init__(self) -> None:

        super().__init__(
            root_item=game.menus.MenuPanel(
                padding_vertical=2,
                padding_horizontal=2,
                child_item=game.menus.ListMenu(
                    items=build_main_menu_items(self.new_game, self.continue_, self.quit),
                    selected=0
                )
            ),
            x=2,
            y=2
        )

    @staticmethod
    def continue_() -> StateResult:
        return Reset(InGame(g.player.current_room_id))

    @staticmethod
    def new_game() -> StateResult:
        return Reset(InGame(g.player.current_room_id))

    @staticmethod
    def quit() -> StateResult:
        raise SystemExit


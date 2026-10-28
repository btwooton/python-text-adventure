from __future__ import annotations

import attrs

from typing import Literal

from game.ui_helpers import get_colored_string

# custom type for room exit directions
Direction = Literal["NORTH", "SOUTH", "EAST", "WEST"]

@attrs.define()
class Entity:

    id: str
    name: str
    description: str

@attrs.define()
class Item(Entity):

    is_gettable: bool
    contents: dict[str, Item] = attrs.field(factory=dict)

@attrs.define()
class Room(Entity):

    exits: dict[str, Direction] = attrs.field(factory=dict)
    items: dict[str, Item] = attrs.field(factory=dict)

    def add_exit(self, direction: Direction, room_id: str):
        self.exits[direction] = room_id

    def get_description(self):
        full_description = (
            f"You are in {self.name}. " +
            self.description
        )
        for _, item in self.items.items():
            full_description += f" There is a {get_colored_string(item.name, 255, 255, 0)} here. " + item.description
        return full_description


@attrs.define()
class Player(Entity):

    current_room_id: str
    inventory: dict[str, Item] = attrs.field(factory=dict)


from __future__ import annotations

from typing import Literal

# custom type for room exit directions
Direction = Literal["NORTH", "SOUTH", "EAST", "WEST"]

class Entity:

    def __init__(self, id: str, name: str, description: str) -> None:
        self.id = id
        self.name = name
        self.description = description

class Item(Entity):

    def __init__(self, id, name, description, is_gettable: bool = False) -> None:
        super().__init__(
            id, name, description
        )
        self.is_gettable = is_gettable
        self.contents = {}

class Room(Entity):

    def __init__(self, id, name, description):
        super().__init__(
            id, name, description
        )
        self.exits = {}
        self.items = {}

    def add_exit(self, direction: Direction, room_id: str):
        self.exits[direction] = room_id

    def get_description(self):
        full_description = (
            f"You are in {self.name}. " +
            self.description
        )
        for _, item in self.items.items():
            full_description += f" There is a {item.name} here. " + item.description
        return full_description


class Player:

    def __init__(self, current_room_id: str) -> None:
        self.current_room_id = current_room_id
        self.inventory = {}


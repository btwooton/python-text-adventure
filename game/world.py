from __future__ import annotations

import attrs

from game.models import Room, Item

class GameWorld:

    def __init__(self) -> None:
        self.rooms = {}

    def load_world(self) -> Room:
        self.rooms["lobby"] = Room(
            "lobby", "The Main Lobby",
            "It's cold and dark."
        )

        self.rooms["hallway"] = Room(
            "hallway",
            "a Long Hallway",
            "Dust floats in the air."
        )

        self.rooms["janitors_closet"] = Room(
            "janitors_closet",
            "a dark and dusty Janitors Closet",
            "You begin sneezing uncontrollably."
        )

        self.rooms["up_staircase"] = Room(
            "up_staircase",
            "a large wooden staircase with a red carpeted runner",
            "The stairs ascend into misty darkness." 
        )

        self.rooms["lobby"].add_exit("NORTH", "hallway")
        self.rooms["hallway"].add_exit("SOUTH", "lobby")
        self.rooms["hallway"].add_exit("NORTH", "up_staircase")
        self.rooms["up_staircase"].add_exit("SOUTH", "hallway")
        self.rooms["lobby"].add_exit("WEST", "janitors_closet")
        self.rooms["janitors_closet"].add_exit("EAST", "lobby")

        self.rooms["lobby"].items["brass_key"] = Item("brass_key", "a brass key", "It looks old.", is_gettable=True)
        self.rooms["janitors_closet"].items["broom"] = Item("broom", "a wood handled broom", "It looks old.", is_gettable=True)

        return self.rooms["lobby"]

    def get_room(self, room_id: str) -> Room | None:
        return self.rooms.get(room_id, None)
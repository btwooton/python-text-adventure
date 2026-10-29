from __future__ import annotations

import tcod.context
import tcod.tileset
import tcod.console

import game.states
import game.world
import game.models
import g
import game.constants as constants
import game.state_tools



def main() -> None:
    tileset = tcod.tileset.load_tilesheet(
        "data/16x16-RogueYun-AgmEdit.png", columns=16, rows=16,
        charmap=tcod.tileset.CHARMAP_CP437
    )
    tileset += tcod.tileset.procedural_block_elements(shape=tileset.tile_shape)
    g.console = tcod.console.Console(constants.CONSOLE_WIDTH, constants.CONSOLE_HEIGHT)
    g.states = [game.states.PaneledMainMenu()]

    # initialize the game world
    g.world = game.world.GameWorld()
    g.player = game.models.Player(
        id="player",
        name="The Player",
        description="The intrepid hero of the story",
        current_room_id=g.world.load_world().id
    )
    g.narrative.append(g.world.get_room(g.player.current_room_id).get_description())
    with tcod.context.new(console=g.console, tileset=tileset) as g.context:
        game.state_tools.main_loop()

if __name__ == '__main__':
    main()
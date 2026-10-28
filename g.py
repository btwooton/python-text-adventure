from __future__ import annotations

import tcod.context
import game.state
import game.world
import game.models

context: tcod.context.Context

console: tcod.console.Console

states: list[game.state.State] = [] # stack of states with top active 

world: game.world.GameWorld

player: game.models.Player
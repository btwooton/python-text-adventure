from __future__ import annotations

from typing import Final

from tcod.event import KeySym
import tcod.tileset

DIRECTION_KEYS: Final = {
    # Arrow keys
    KeySym.LEFT: (-1, 0),
    KeySym.RIGHT: (1, 0),
    KeySym.UP: (0, -1),
    KeySym.DOWN: (0, 1),
    # Keypad
    KeySym.KP_4: (-1, 0),
    KeySym.KP_6: (1, 0),
    KeySym.KP_8: (0, -1),
    KeySym.KP_2: (0, 1),
    # VI keys
    KeySym.h: (-1, 0),
    KeySym.l: (1, 0),
    KeySym.k: (0, -1),
    KeySym.j: (0, 1),
}

CONSOLE_WIDTH = 60
CONSOLE_HEIGHT = 40

cmap = lambda code: tcod.tileset.CHARMAP_CP437[code]

# constants for outline tiles
OUTLINE_HORIZONTAL = cmap(196)
OUTLINE_VERTICAL = cmap(179)
OUTLINE_TOP_LEFT = cmap(218)
OUTLINE_TOP_RIGHT = cmap(191)
OUTLINE_BOTTOM_LEFT = cmap(192)
OUTLINE_BOTTOM_RIGHT = cmap(217)

FRAME_DECORATION = (
    OUTLINE_TOP_LEFT,
    OUTLINE_HORIZONTAL,
    OUTLINE_TOP_RIGHT,
    OUTLINE_VERTICAL,
    ord(' '),
    OUTLINE_VERTICAL,
    OUTLINE_BOTTOM_LEFT,
    OUTLINE_HORIZONTAL,
    OUTLINE_BOTTOM_RIGHT
)

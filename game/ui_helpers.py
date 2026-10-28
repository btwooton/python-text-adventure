from __future__ import annotations

from tcod import libtcodpy

def get_colored_string(text: str, r: int, g: int, b: int) -> str:
    return f"{libtcodpy.COLCTRL_FORE_RGB:c}{r:c}{g:c}{b:c}{text}{libtcodpy.COLCTRL_STOP:c}"
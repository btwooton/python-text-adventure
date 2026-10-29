from __future__ import annotations

from tcod import libtcodpy
import re

def get_colored_string(text: str, r: int, g: int, b: int) -> str:
    return f"{libtcodpy.COLCTRL_FORE_RGB:c}{r:c}{g:c}{b:c}{text}{libtcodpy.COLCTRL_STOP:c}"

def strip_coloration(text: str) -> str:
    result_text = ""
    start_pattern = rf"{libtcodpy.COLCTRL_FORE_RGB:c}" + rf"[{0:c}-{255:c}]" * 3
    end_pattern = rf"{libtcodpy.COLCTRL_STOP:c}"
    start_match = re.search(start_pattern, text)

    if start_match is not None:
        result_text = text[:start_match.span()[0]]
        result_text += text[start_match.span()[1]+2:]
    else:
        result_text = text

    end_match = re.search(end_pattern, result_text)

    if end_match is not None:
        result_text = (
            result_text[:end_match.span()[0]] + 
            result_text[end_match.span()[1]:]
        )
    else:
        result_text = text

    return result_text
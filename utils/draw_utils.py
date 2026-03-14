from pathlib import Path
from PIL import ImageFont


_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_FONTS_DIR = _PROJECT_ROOT / "fonts"

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_word = ""

    for word in words:
        temp = current_word + (" " if current_word else "") + word
        width = font.getlength(temp)
        if width <= max_width:
            current_word = temp
        else: 
            if current_word:
                lines.append(current_word)
            current_word = word

    if current_word:
        lines.append(current_word)

    return lines

serif_font = str(_FONTS_DIR / "literata.ttf")
sans_font = str(_FONTS_DIR / "googlesans.ttf")
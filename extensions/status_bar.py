from PIL import Image, ImageDraw, ImageFont

from utils.draw_utils import sans_font


class StatusBar:
    def __init__(self, width: int, height: int = 24, background=(255, 255, 255), text_color=(0, 0, 0)):
        self.width = width
        self.height = height
        self.background = background
        self.text_color = text_color
        self._texts: dict[str, str] = {}
        self._font = ImageFont.truetype(sans_font, 13)

    def clear(self):
        self._texts.clear()

    def set_text(self, source: str, text: str):
        self._texts[source] = text

    def render(self) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height), self.background)
        draw = ImageDraw.Draw(img)

        bar_text = " | ".join(value for value in self._texts.values() if value)
        if bar_text:
            draw.text((8, 0), bar_text, fill=self.text_color, font=self._font)

        draw.line((0, 0, self.width, 0), fill=self.text_color, width=1)
        return img
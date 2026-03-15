from PIL import Image, ImageDraw, ImageFont
from utils.draw_utils import *


class WeatherPlugin:
    def __init__(self, config, width, height, status_bar=None):
        self.width = width
        self.height = height
        self.config = config
        self.status_bar = status_bar

    async def update(self):
        if self.status_bar:
            self.status_bar.set_text("weather", "Weather: updated")

    async def render(self) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        draw.text((20, 20), "Hi from weather plugin!", fill=(0, 0, 0), font=ImageFont.truetype(serif_font, 15))
        draw.rectangle((0, 0, self.width, self.height), outline=(0, 0, 0), width=5)
        return img
from PIL import Image, ImageDraw, ImageFont
from utils.draw_utils import *

class WeatherPlugin:
    def __init__(self, config, width, height):
        self.width = width
        self.height = height
        self.config = config

    async def update(self):...

    async def render(self) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        draw.text((20, 20), "Hi from weather plugin!", fill=(0, 0, 0), font=ImageFont.truetype(serif_font, 15))

        return img
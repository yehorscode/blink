from .base import BaseDisplay
from PIL import Image
import time


class WaveshareDisplay(BaseDisplay):
    WIDTH = 250
    HEIGHT = 122

    def init(self):
        from waveshare_epd import epd2in13_V4
        self.epd = epd2in13_V4.EPD()
        self.epd.init()

    def display(self, image: Image.Image):
        bw = image.convert("1").resize((self.WIDTH, self.HEIGHT))
        self.epd.display(self.epd.getbuffer(bw))

    def clear(self):
        self.epd.Clear()

    def wait(self, seconds: float | None = None):
        if seconds is not None:
            time.sleep(seconds)

    def sleep(self):
        self.epd.sleep()
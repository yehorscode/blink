from .base import BaseDisplay
from PIL import Image
import time

class WaveshareDisplay(BaseDisplay):
    def init(self): raise NotImplementedError
    def display(self, image: Image.Image): raise NotImplementedError
    def clear(self): raise NotImplementedError
    def wait(self, seconds: float | None = None):
        if seconds is not None:
            time.sleep(seconds)
    def sleep(self): raise NotImplementedError
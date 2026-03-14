from abc import ABC, abstractmethod
from PIL import Image

class BaseDisplay(ABC):
    width = 400
    height = 300

    def __init__(self):
        self.canvas = Image.new("RGB", (self.width, self.height), (255, 255, 255))

    @abstractmethod
    def init(self): ...

    def get_canvas(self) -> Image.Image:
        return self.canvas

    @abstractmethod
    def display(self, image: Image.Image): ...

    @abstractmethod
    def clear(self): ...

    @abstractmethod
    def wait(self, seconds: float | None = None): ...

    @abstractmethod
    def sleep(self): ...

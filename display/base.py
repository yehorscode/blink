from abc import ABC, abstractmethod
from PIL import Image

class BaseDisplay(ABC):
    width = 400
    height = 300

    @abstractmethod
    def init(self): ...

    @abstractmethod
    def display(self, image: Image.Image): ...

    @abstractmethod
    def clear(self): ...

    @abstractmethod
    def wait(self, seconds: float | None = None): ...

    @abstractmethod
    def sleep(self): ...

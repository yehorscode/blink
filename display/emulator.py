import pygame
from PIL import Image
from .base import BaseDisplay

class EmulatorDisplay(BaseDisplay):
    scale = 2
    refresh_flash_ms = 120

    def init(self):
        pygame.init()
        w = self.width * self.scale
        h = self.height * self.scale
        self.screen = pygame.display.set_mode((w,h))
        self.screen.fill((220,218,210))
        pygame.display.flip()
    
    def display(self,image:Image.Image):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.sleep()
    
        self.screen.fill((0,0,0))
        pygame.display.flip()
        pygame.time.wait(self.refresh_flash_ms)

        img = image.convert("RGB").resize(
            (self.width * self.scale, self.height * self.scale),
            resample=Image.Resampling.NEAREST
        )

        surface = pygame.image.fromstring(img.tobytes(), img.size,"RGB")
        self.screen.blit(surface, (0, 0))
        pygame.display.flip()
    
    def clear(self):
        self.display(Image.new("RGB", (self.width, self.height), (255,255,255)))

    def wait(self, seconds: float | None = None):
        clock = pygame.time.Clock()
        start_ms = pygame.time.get_ticks()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            if seconds is not None:
                elapsed_ms = pygame.time.get_ticks() - start_ms
                if elapsed_ms >= int(seconds * 1000):
                    return

            clock.tick(60)
    
    def sleep(self):
        pygame.quit()
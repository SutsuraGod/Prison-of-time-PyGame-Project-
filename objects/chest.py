import assets
import pygame


class Chest(pygame.sprite.Sprite):
    def __init__(self, sdv, *groups):
        super().__init__(*groups)

        self.image = assets.load_sprite('chest_closed.jpg', -1)
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.topleft = sdv
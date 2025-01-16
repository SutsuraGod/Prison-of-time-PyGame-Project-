import assets
import pygame


class Door(pygame.sprite.Sprite):
    def __init__(self, sdv, *groups):
        super().__init__(*groups)
        
        self.image = assets.load_sprite('door_opened.png')
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.topleft = sdv
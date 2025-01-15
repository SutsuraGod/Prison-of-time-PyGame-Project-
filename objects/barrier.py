import assets
import pygame


class Barrier(pygame.sprite.Sprite):
    def __init__(self, sdv, *groups):
        super().__init__(*groups)

        self.image = assets.load_sprite('wall_down.png')
        #self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        self.rect.center = sdv


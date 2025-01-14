import assets
import pygame


class Void(pygame.sprite.Sprite):
    def __init__(self, sdv, *groups):
        super().__init__(*groups)

        self.image = assets.load_sprite('stoneage_stone_texture.jpg')

        self.rect = self.image.get_rect()
        self.rect.center = sdv
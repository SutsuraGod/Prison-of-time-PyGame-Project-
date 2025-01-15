import assets
import pygame
import random

class Void(pygame.sprite.Sprite):
    def __init__(self, sdv, *groups):
        super().__init__(*groups)

        skins = ["void_1.jpg", "void_2.jpg", "void_3.jpg", "void_4.jpg"]

        self.image = assets.load_sprite(skins[random.randint(0, 3)])

        self.rect = self.image.get_rect()
        self.rect.center = sdv
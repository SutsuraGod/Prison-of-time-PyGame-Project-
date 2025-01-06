import assets
import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
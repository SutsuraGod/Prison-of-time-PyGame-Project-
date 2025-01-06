import assets
import pygame


class Chest(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
import assets
import pygame


class Barrier(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
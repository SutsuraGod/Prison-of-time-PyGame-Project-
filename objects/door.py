import assets
import pygame


class Door(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
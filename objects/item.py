import assets
import pygame
import groups


class Item(pygame.sprite.Sprite):
    def __init__(self, position, item_type, *groups):
        super().__init__(*groups)
        self.type = item_type
        if self.type == 'fireball':
            self.image = assets.load_sprite('fireball.png', -1)
        elif self.type == 'speed':
            self.image = assets.load_sprite('speed.png')
        elif self.type == 'health':
            self.image = assets.load_sprite('hp.png')
        elif self.type == 'icespell':
            self.image = assets.load_sprite('icespell.png', -1)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=position)
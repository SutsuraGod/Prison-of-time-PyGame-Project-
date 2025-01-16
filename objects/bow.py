import assets
import pygame
import configs
import math


class Bow(pygame.sprite.Sprite):
    def __init__(self, player_pos, *groups):
        self.start_image = assets.load_sprite('bow.png', colorkey=-1)
        self.start_rect = self.start_image.get_rect(topleft=(player_pos[0], player_pos[1] + 10))

        self.angle = 0
        self.image = self.start_image
        self.rect = self.image.get_rect(center=self.start_rect.center)
        self.mask = pygame.mask.Mask((10, 10))
        super().__init__(*groups)

    def update(self, player_pos, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        self.start_rect.center = player_pos[0], player_pos[1] + 10
        self.angle = math.degrees(math.atan2(mouse_y - self.start_rect.centery, mouse_x - self.start_rect.centerx))
        self.image = pygame.transform.rotate(self.start_image, -self.angle + 225)
        self.rect = self.image.get_rect(center=(player_pos[0], player_pos[1] + 10))
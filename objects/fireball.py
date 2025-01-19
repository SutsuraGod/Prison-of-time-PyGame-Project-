import pygame
import assets
from objects.projectile import Projectile
import math


class Fireball(Projectile):
    def __init__(self, filename, spawn_pos, target_pos, normal_angle, groups):
        super().__init__(filename, spawn_pos, target_pos, normal_angle, *groups)
        self.start_image = assets.load_sprite(filename, colorkey=-1)
        self.start_image = pygame.transform.scale(self.start_image, (40, 40))
        self.start_rect = self.start_image.get_rect(center=spawn_pos)

        self.normal_angle = normal_angle
        self.angle = math.degrees(math.atan2(self.target_y - self.start_rect.centery, self.target_x - self.start_rect.centerx))
        self.image = pygame.transform.rotate(self.start_image, -self.angle + self.normal_angle)
        self.rect = self.image.get_rect(center=self.start_rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        return super().update()
    
    def damage(self, obj):
        obj.health -= 2
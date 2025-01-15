import assets
import pygame
import configs
import math
from groups import collis

class Arrow(pygame.sprite.Sprite):
    def __init__(self, spawn_pos, target_pos, *groups):
        super().__init__(*groups)
        self.start_x, self.start_y = spawn_pos[0], spawn_pos[1]
        self.cur_x, self.cur_y = spawn_pos[0], spawn_pos[1]
        self.target_x, self.target_y = target_pos[0], target_pos[1]
        self.speed = 360 // configs.FPS

        self.start_image = assets.load_sprite('arrow.png', colorkey=-1)
        self.start_rect = self.start_image.get_rect(center=spawn_pos)

        self.mask = pygame.mask.from_surface(self.start_image)

        self.angle = math.degrees(math.atan2(self.target_y - self.start_rect.centery, self.target_x - self.start_rect.centerx))
        self.image = pygame.transform.rotate(self.start_image, -self.angle + 45)
        self.rect = self.image.get_rect(center=self.start_rect.center)
    
    def update(self):
        if (self.cur_x >= 0 and self.cur_x <= configs.SCREEN_WIDTH
                and self.cur_y >= 0 and self.cur_y <= configs.SCREEN_HEIGHT):
            
            delta_x = self.target_x - self.start_x
            delta_y = self.target_y - self.start_y

            distance = (delta_x**2 + delta_y**2) ** 0.5

            step_x = self.speed * delta_x / distance
            step_y = self.speed * delta_y / distance

            self.cur_x += step_x
            self.cur_y += step_y
            self.rect.center = self.cur_x, self.cur_y

            if pygame.sprite.spritecollide(self, collis, False):
                self.kill()

        else:    
            self.kill()

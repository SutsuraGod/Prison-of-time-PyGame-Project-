import pygame
import random
import configs
from groups import all_sprites
from pygame.math import Vector2

class Bullet(pygame.sprite.Sprite):
    def __init__(self, boss_pos, player_pos, speed=5, deviation=0.2):
        super().__init__(all_sprites)
        self.speed = speed
        self.deviation = deviation

        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 0), (5, 5), 5)
        self.rect = self.image.get_rect(center=boss_pos)

        player_pos = (player_pos[0] + random.randint(-100, 100), player_pos[1] + random.randint(-100, 100))
        print(player_pos)

        direction = Vector2(player_pos) - Vector2(boss_pos)
        angle = random.uniform(-deviation, deviation)
        self.direction = direction.rotate(angle).normalize()

        self.direction.x += self.direction.x * random.random()
        self.direction.y += self.direction.y * random.random()

        self.speed = 7 * random.random() + 3

    def update(self, player):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        if pygame.sprite.collide_rect(self, player):
            player.health -= 1
            print(f"Player hit! Health: {player.health}")
            self.kill()

        if (self.rect.x < 0 or self.rect.x > configs.SCREEN_WIDTH or
                self.rect.y < 0 or self.rect.y > configs.SCREEN_HEIGHT):
            self.kill()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
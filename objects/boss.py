import pygame
import random
import configs
import time
import groups
from objects.bullet import Bullet
from pygame.math import Vector2

from PIL import Image, ImageSequence


def load_gif_frames(path):
    gif = Image.open(path)
    frames = []
    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert("RGBA")
        data = frame.getdata()
        new_data = []
        for item in data:
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        frame.putdata(new_data)
        pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
        frames.append(pygame_image)
    return frames


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.start_health = 20
        self.start_speed = 90 // configs.FPS
        self.health = self.start_health
        self.speed = self.start_speed

        self.frames = load_gif_frames(r"data\sprites\vrag.gif")
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.mask = pygame.mask.from_surface(self.image)

        self.animation_counter = 0
        self.animation_speed = 10

        self.last_shoot = time.time()

        self.direction = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.change_time = pygame.time.get_ticks() + random.randint(10000, 30000)

        self.min_distance_to_player = 500

    def update_animation(self):
        '''Анимация'''
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.mask = pygame.mask.from_surface(self.image)

    def move(self, player, player_rect, enemy_type, obstacles, player_pos):
        '''Движение босса и стрельба'''
        if time.time() - self.last_shoot > 3:
            for i in range(7):
                bullet = Bullet(self.rect.center, player.rect.center)
                groups.all_sprites.add(bullet)
                self.last_shoot = time.time()

        if self.health <= 0:
            groups.current_level.enemies.remove(self)
            self.kill()
            return

        to_player = Vector2(player_rect.centerx - self.rect.centerx,
                            player_rect.centery - self.rect.centery)
        distance_to_player = to_player.length()

        if distance_to_player > self.min_distance_to_player:
            self.direction = to_player.normalize()
        else:
            self.direction = -to_player.normalize()

        for obstacle in obstacles:
            if pygame.sprite.collide_mask(self, obstacle):
                self.avoid_obstacle(obstacle)
                return

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        self.rect.x = max(50, min(self.rect.x, configs.SCREEN_WIDTH - self.rect.width - 50))
        self.rect.y = max(50, min(self.rect.y, configs.SCREEN_HEIGHT - self.rect.height - 50))

        self.update_animation()

    def avoid_obstacle(self, obstacle):
        '''Обход препятствий'''
        offset = 5.5
        new_direction = self.direction.rotate(135)
        new_position = self.rect.center + new_direction * offset

        new_position.x = max(70, min(new_position.x, configs.SCREEN_WIDTH - 70))
        new_position.y = max(70, min(new_position.y, configs.SCREEN_HEIGHT - 70))

        self.rect.center = new_position
        self.direction = new_direction
import assets
import pygame
import configs
import groups
from objects.item import Item
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        self.health = 5
        self.right_images = [
            assets.load_sprite('player1.png', colorkey=-1),
            assets.load_sprite('player2.png', colorkey=-1),
            assets.load_sprite('player3.png', colorkey=-1),
            assets.load_sprite('player4.png', colorkey=-1),
            assets.load_sprite('player5.png', colorkey=-1),
            assets.load_sprite('player6.png', colorkey=-1),
        ]
        self.left_images = [
            pygame.transform.flip(image, True, False) for image in self.right_images
        ]
        self.image = self.right_images[0]
        self.direction = True
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.counter_images = 0

        super().__init__(*groups)
        self.speed = 0
        self.max_v = 360 / configs.FPS
        self.a = 5 / configs.FPS

        self.rect.x = x
        self.rect.y = y

        self.current_spell = ''

        self.max_health = 7
        self.max_speed = 540 // configs.FPS
        self.step_speed = 0
        self.step_health = 0
        self.default_health = 5
        self.default_speed = 0

    def update(self, mouse_pos):
        if self.health <= 0:
            self.kill()

        x = mouse_pos[0]
        if x < self.rect.centerx:
            if self.counter_images % 6 == 0:
                self.left_images.append(self.left_images.pop(0))
                self.image = self.left_images[0]
            self.counter_images += 1
        else:
            if self.counter_images % 6 == 0:
                self.right_images.append(self.right_images.pop(0))
                self.image = self.right_images[0]
            self.counter_images += 1

    def moving_event(self, keys):

        was_x = self.rect.x
        was_y = self.rect.y

        if self.speed < self.max_v:
            self.speed += self.a
        if keys[pygame.K_w] and keys[pygame.K_d]:
            self.rect.x += self.speed / (2 ** 0.5)
            self.rect.y -= self.speed / (2 ** 0.5)
            self.direction = True
        elif keys[pygame.K_d] and keys[pygame.K_s]:
            self.rect.x += self.speed / (2 ** 0.5)
            self.rect.y += self.speed / (2 ** 0.5)
            self.direction = True
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            self.rect.x -= self.speed / (2 ** 0.5)
            self.rect.y += self.speed / (2 ** 0.5)
            self.direction = False
        elif keys[pygame.K_a] and keys[pygame.K_w]:
            self.rect.x -= self.speed / (2 ** 0.5)
            self.rect.y -= self.speed / (2 ** 0.5)
            self.direction = False
        elif keys[pygame.K_w]:
            self.rect.y -= self.speed
        elif keys[pygame.K_s]:
            self.rect.y += self.speed
        elif keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.direction = False
        elif keys[pygame.K_d]:
            self.rect.x += self.speed
            self.direction = True
        
        if groups.current_level:
            for sprite in groups.current_level.objects:
                if pygame.sprite.collide_mask(self, sprite):
                    self.rect.x = was_x
                    self.rect.y = was_y
                
        for door in groups.doors:
            if pygame.sprite.collide_rect(self, door):
                if door.get_status():
                    if len(groups.levels) > groups.levels.index(groups.current_level) + 1 and configs.SCREEN_WIDTH // 2 < self.rect.x:
                        groups.current_level = groups.levels[groups.levels.index(groups.current_level) + 1]
                        self.update_position((configs.SCREEN_WIDTH // configs.CELL_SIZE) * 2, (configs.SCREEN_HEIGHT // configs.CELL_SIZE) * 19)
                    elif len(groups.levels) > groups.levels.index(groups.current_level) - 1 and configs.SCREEN_WIDTH // 2 > self.rect.x:
                        groups.current_level = groups.levels[groups.levels.index(groups.current_level) - 1]
                        self.update_position((configs.SCREEN_WIDTH // configs.CELL_SIZE) * 34, (configs.SCREEN_HEIGHT // configs.CELL_SIZE) * 19)
                    groups.arrow_sprites.empty()
                    groups.spell_sprites.empty()
                    break

        for item in groups.current_level.items:
            if pygame.sprite.collide_rect(self, item):
                if item.type == 'speed' and self.max_speed > self.speed:
                    self.set_speed(30)
                    groups.current_level.items.remove(item)
                elif item.type == 'health' and self.max_health != self.health:
                    self.set_health(1)
                    groups.current_level.items.remove(item)
                elif item.type == 'fireball' or item.type == 'icespell':
                    self.set_spell(item.type)
                    groups.current_level.items.remove(item)

    def update_position(self, new_x, new_y):
        self.rect.x = new_x
        self.rect.y = new_y

    def set_speed(self, new_speed):
        if self.speed < self.max_speed:
            self.speed += (new_speed / configs.FPS) * math.exp(-self.step_speed)

    def set_health(self, new_health):
        if self.health < self.max_health:
            self.health += new_health

    def set_spell(self, new_spell):
        if self.current_spell != new_spell:
            if self.current_spell != '':
                if self.direction:
                    groups.current_level.items.append(
                        Item((self.rect.centerx - 70, self.rect.centery), self.current_spell,
                            (groups.items_sprite, groups.all_sprites))
                    )
                else:
                    groups.current_level.items.append(
                        Item((self.rect.centerx + 70, self.rect.centery), self.current_spell,
                            (groups.items_sprite, groups.all_sprites))
                    )
            self.current_spell = new_spell

    def set_default_stats(self):
        self.health = self.default_health
        self.speed = self.default_speed
        self.current_spell = ''
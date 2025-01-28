import assets
import pygame
import configs
import groups
from objects.item import Item
import math
from sound_manager import play_sound


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
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.counter_images = 0

        super().__init__(*groups)
        self.v = 0
        self.max_v = 360 / configs.FPS
        self.a = 5 / configs.FPS

        self.rect.x = x
        self.rect.y = y

        self.current_spell = ''

        self.max_health = 7
        self.max_speed = 540 // configs.FPS
        self.step_speed = 0
        self.step_health = 0

        self.last_attack_time = 0
        self.last_spelling_time = 0

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
        was_x, was_y = self.rect.x, self.rect.y
        dx, dy = 0, 0

        if self.v < self.max_v:
            self.v += self.a
        if keys[pygame.K_w]:
            dy -= self.v
        if keys[pygame.K_s]:
            dy += self.v
        if keys[pygame.K_a]:
            dx -= self.v
            self.direction = False
        if keys[pygame.K_d]:
            dx += self.v
            self.direction = True

        # Диагональное движение
        if dx != 0 and dy != 0:
            diagonal_speed = self.v / (2 ** 0.5)
            dx *= diagonal_speed / self.v
            dy *= diagonal_speed / self.v

        # Проверяем движение по X
        self.rect.x += dx
        for sprite in groups.current_level.objects:
            if pygame.sprite.collide_mask(self, sprite):
                self.rect.x = was_x
                break

        # Проверяем движение по Y
        self.rect.y += dy
        for sprite in groups.current_level.objects:
            if pygame.sprite.collide_mask(self, sprite):
                self.rect.y = was_y
                break
                
        for door in groups.current_level.doors:
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
                if item.type == 'speed' and self.max_speed > self.v:
                    self.set_speed(30)
                    groups.current_level.items.remove(item)
                    play_sound('item')
                elif item.type == 'health' and self.max_health != self.health:
                    self.set_health(1)
                    groups.current_level.items.remove(item)
                    play_sound('item')
                elif item.type == 'fireball' or item.type == 'icespell':
                    if item.type != self.current_spell:
                        self.set_spell(item.type)
                        groups.current_level.items.remove(item)
                        play_sound('item')

    def update_position(self, new_x, new_y):
        self.rect.x = new_x
        self.rect.y = new_y

    def set_speed(self, new_speed):
        if self.v < self.max_speed:
            self.v += (new_speed / configs.FPS) * math.exp(-self.step_speed)

    def set_health(self, new_health):
        if self.health < self.max_health:
            self.health += new_health

    def set_spell(self, new_spell):
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
    
    def get_collision_side(self, obstacle_rect):
        # Вычисляем разницу между сторонами
        dx = (self.rect.centerx - obstacle_rect.centerx - 1)
        dy = (self.rect.centery - obstacle_rect.centery - 1)
        print(dx, dy)
        # Сравниваем абсолютные значения
        if abs(dx) > abs(dy):
            if dx > 0:
                return "left"  # Столкновение с левой стороны препятствия
            else:
                return "right"  # Столкновение с правой стороны препятствия
        else:
            if dy > 0:
                return "top"  # Столкновение с верхней стороны препятствия
            else:
                return "bottom"  # Столкновение с нижней стороны препятствия
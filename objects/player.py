import assets
import pygame
import configs
import groups


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        # self.level = level
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
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.counter_images = 0

        super().__init__(*groups)
        self.v = 0
        self.max_v = 360 / configs.FPS
        self.a = 5 / configs.FPS

        self.rect.x = x
        self.rect.y = y

    def update(self, mouse_pos):
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

        if self.v < self.max_v:
            self.v += self.a
        if keys[pygame.K_w] and keys[pygame.K_d]:
            self.rect.x += self.v / (2 ** 0.5)
            self.rect.y -= self.v / (2 ** 0.5)
        elif keys[pygame.K_d] and keys[pygame.K_s]:
            self.rect.x += self.v / (2 ** 0.5)
            self.rect.y += self.v / (2 ** 0.5)
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            self.rect.x -= self.v / (2 ** 0.5)
            self.rect.y += self.v / (2 ** 0.5)
        elif keys[pygame.K_a] and keys[pygame.K_w]:
            self.rect.x -= self.v / (2 ** 0.5)
            self.rect.y -= self.v / (2 ** 0.5)
        elif keys[pygame.K_w]:
            self.rect.y -= self.v
        elif keys[pygame.K_s]:
            self.rect.y += self.v
        elif keys[pygame.K_a]:
            self.rect.x -= self.v
        elif keys[pygame.K_d]:
            self.rect.x += self.v
        
        if groups.current_level:
            for sprite in groups.current_level.objects:
                if pygame.sprite.collide_mask(self, sprite):
                    self.rect.x = was_x
                    self.rect.y = was_y
                
        for door in groups.doors:
            if pygame.sprite.collide_rect(self, door):
                if len(groups.levels) > groups.levels.index(groups.current_level) + 1 and configs.SCREEN_WIDTH // 2 < self.rect.x:
                    groups.current_level = groups.levels[groups.levels.index(groups.current_level) + 1]
                    self.update_position((configs.SCREEN_WIDTH // configs.CELL_SIZE) * 2, (configs.SCREEN_HEIGHT // configs.CELL_SIZE) * 19)
                elif len(groups.levels) > groups.levels.index(groups.current_level) - 1 and configs.SCREEN_WIDTH // 2 > self.rect.x:
                    groups.current_level = groups.levels[groups.levels.index(groups.current_level) - 1]
                    self.update_position((configs.SCREEN_WIDTH // configs.CELL_SIZE) * 34, (configs.SCREEN_HEIGHT // configs.CELL_SIZE) * 19)
                groups.arrow_sprites.empty()
                groups.spell_sprites.empty()
                break

    def update_position(self, new_x, new_y):
        self.rect.x = new_x
        self.rect.y = new_y
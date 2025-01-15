import assets
import pygame
import configs
from groups import items


class Player(pygame.sprite.Sprite):
    def __init__(self, level, x, y, *groups):
        self.level = level
        self.mask = pygame.mask.Mask((10, 10))
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
        
        # new_x = self.rect.x
        # new_y = self.rect.y

        # if pygame.sprite.spritecollide(self, self.level.collision(), dokill=False):
        #     self.rect.x = was_x
        #     self.rect.y = was_y
        for sprite in items:
            if pygame.sprite.collide_mask(self, sprite):
                self.rect.x = was_x
                self.rect.y = was_y

            

        #     now_x = was_x
        #     now_y = was_y

        #     while (new_x - was_x) or (new_y - was_y):

        #         self.rect.x = now_x
        #         self.rect.y = now_y

        #         if not pygame.sprite.spritecollide(self, self.level.collision(), dokill=False):

        #             now_x += (new_x - was_x) * 0.01
        #             now_y += (new_y - was_y) * 0.01
                
        #         else:

        #             now_x -= (new_x - was_x) * 0.01
        #             now_y -= (new_y - was_y) * 0.01
        #             break
            
        #     print(now_x, now_y)

        #     self.rect.x = now_x
        #     self.rect.y = now_y
    
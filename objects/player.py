import assets
import pygame
import configs


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self.image = assets.load_sprite('player.png', colorkey=-1)
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.flip = False
        super().__init__(*groups)

        self.v = 0
        self.max_v = 360 / configs.FPS
        self.a = 5 / configs.FPS

    def update(self, mouse_pos):
        x = mouse_pos[0]
        if ((self.flip and x >= self.rect.centerx) or (not self.flip and x < self.rect.centerx)):
            self.image = pygame.transform.flip(self.image, True, False)
        if x < self.rect.centerx:
            self.flip = True
        else:
            self.flip = False
        

    def moving_event(self, keys):
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
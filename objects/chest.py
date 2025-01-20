import assets
import pygame
from objects.item import Item
import random
import groups


class Chest(pygame.sprite.Sprite):
    def __init__(self, sdv, *groups):
        super().__init__(*groups)

        self.image = assets.load_sprite('chest_closed.png', -1)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.topleft = sdv
        self.opened = False
        self.drop = ['fireball']

    def update(self, player_pos, keys, screen):
        x, y = player_pos
        if ((x - self.rect.centerx) ** 2 + (y - self.rect.centery) ** 2) ** 0.5 <= 75:
            if not self.opened:
                interact_image = assets.load_sprite('kb_e.png')
                interact_image = pygame.transform.scale(interact_image, (40, 40))
                interact_image_rect = interact_image.get_rect(center=self.rect.center)
                screen.blit(interact_image, (interact_image_rect.centerx - 20, interact_image_rect.centery - 50))
                if keys[pygame.K_e]:
                    self.open()
                    self.opened = True

    def open(self):
        self.image = assets.load_sprite('chest_opened.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        item = random.sample(self.drop, 1)
        print(item)
        groups.current_level.items.append(Item((self.rect.centerx, self.rect.centery + 20), item[0],
                                        (groups.items_sprite, groups.all_sprites)))

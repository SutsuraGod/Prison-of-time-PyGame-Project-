import assets
import pygame
import groups


class Item(pygame.sprite.Sprite):
    def __init__(self, position, item_type, *groups):
        super().__init__(*groups)
        self.type = item_type
        if self.type == 'fireball':
            self.image = assets.load_sprite('fireball.png', -1)
        elif self.type == 'speed':
            self.image = assets.load_sprite('speed.png')
        elif self.type == 'health':
            self.image = assets.load_sprite('hp.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=position)

    def update(self, player):
        x, y = player.rect.centerx, player.rect.centery

        if ((x - self.rect.centerx) ** 2 + (y - self.rect.centery) ** 2) ** 0.5 <= 40:
            if self.type == 'speed':
                player.set_speed(60)
            elif self.type == 'health':
                player.set_health(1)
            elif self.type == 'fireball':
                player.set_spell(self.type)
            groups.current_level.items.remove(self)
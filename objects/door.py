import assets
import pygame


class Door(pygame.sprite.Sprite):
    def __init__(self, sdv, *groups):
        super().__init__(*groups)
        
        self.images = [
                        assets.load_sprite('door_opened.png'),
                        assets.load_sprite('door_closed.png')
                       ]
        self.image = self.images[0]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.topleft = sdv

    def update(self, fight):
        '''Дверь закрыта, если в комнате все еще есть враги'''
        if fight:
            self.image = self.images[1]
        else:
            self.image = self.images[0]

    def get_status(self):
        '''Возвращает True если дверь открыта, False - если нет'''
        if self.image == self.images[0]:
            return True
        return False
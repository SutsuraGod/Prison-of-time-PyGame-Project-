import pygame
import configs
from objects.barrier import Barrier
from objects.chest import Chest
from objects.door import Door
from objects.enemy import Enemy
from objects.player import Player
from objects.wall import Wall
from objects.bow import Bow
from objects.arrow import Arrow
from groups import items, collis



class Level():

    def __init__(self, file, screen, all_sprites):
        
        with open(file, encoding="utf-8", mode="r") as fl:
            map = [x.strip() for x in fl.readlines()]

        # self.items = pygame.sprite.Group()
        # self.collis = pygame.sprite.Group()
        
        self.screen = screen
        self.m = len(map[0])
        self.n = len(map)

        self.siz = 40

        for lay in range(0, self.n):
            for pos in range(0, self.m):

                sdv = (pos * self.siz + 80, lay * self.siz + 60)

                if map[lay][pos] == "%":
                    Barrier(sdv, (items, collis, all_sprites))
                if map[lay][pos] == "#":
                    Wall(sdv, (items, collis, all_sprites))

        items.draw(screen)

    def draw(self):
        items.draw(self.screen)

    def collision(self):
        return collis

if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT), pygame.RESIZABLE)
    screen.fill('gray')

    running = True
    lv = Level(r"data\levels\level_46_25.txt", screen)
    while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            screen.fill('gray')
            lv.draw()
            pygame.display.flip()
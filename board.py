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
from objects.void import Void
from groups import items, collis, player_sprites, levels, doors, chests_sprites
from random import sample



class Level():

    def __init__(self, file, screen, all_sprites):
        self.objects = []
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

                sdv = (pos * self.siz, lay * self.siz)

                if map[lay][pos] == "%":
                    self.objects.append(Barrier(sdv, (items, collis, all_sprites)))
                elif map[lay][pos] == "#":
                    self.objects.append(Wall(sdv, (items, collis, all_sprites)))
                # if map[lay][pos] == ".": СКОРЕЕ ВСЕГО МЫ ВООБЩЕ УБЕРЕМ ЭТО!!!
                #     Void(sdv, (items, all_sprites))
                elif map[lay][pos] == '@':
                    if configs.player is None:
                        configs.player = Player(sdv[0], sdv[1], (player_sprites, all_sprites))
                elif map[lay][pos] == '|':
                    self.objects.append(Door(sdv, (items, collis, doors, all_sprites)))
                elif map[lay][pos] == '&':
                    self.objects.append(Chest(sdv, (items, collis, chests_sprites, all_sprites)))


        # items.draw(screen)

    def draw(self):
        for obj in self.objects:
            self.screen.blit(obj.image, obj.rect)

    def collision(self):
        return collis


def generate_level(screen, all_sprites):
    levels.append(Level(f"data/levels/save_levels/start_room.txt", screen, all_sprites))
    for i in sample(range(1, 11), 4):
        levels.append(Level(f'data/levels/room_{i}.txt', screen, all_sprites))
    levels.append(Level(f"data/levels/save_levels/chest_room.txt", screen, all_sprites))


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
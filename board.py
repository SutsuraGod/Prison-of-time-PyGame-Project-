import pygame
import configs
from objects.barrier import Barrier
from objects.chest import Chest
from objects.door import Door
from objects.enemy import Enemy
from objects.player import Player
from objects.wall import Wall
from objects.bow import Bow
from objects.void import Void
from objects.boss1 import Boss
from groups import items, collis, player_sprites, levels, doors, chests_sprites, enemy_sprites
import groups
from random import sample


class Level():
    def __init__(self, file, screen, all_sprites):
        self.objects = []
        self.enemies = []
        self.items = []
        self.chests = []
        self.doors = []
        with open(file, encoding="utf-8", mode="r") as fl:
            map = [x.strip() for x in fl.readlines()]
        
        self.screen = screen
        self.m = len(map[0])
        self.n = len(map)

        self.siz = 40

        for lay in range(0, self.n):
            for pos in range(0, self.m):

                sdv = (pos * self.siz, lay * self.siz)

                if map[lay][pos] == '%':
                    self.objects.append(Barrier(sdv, (items, collis, all_sprites)))
                elif map[lay][pos] == '#':
                    self.objects.append(Wall(sdv, (items, collis, all_sprites)))
                elif map[lay][pos] == '@':
                    if configs.player is None:
                        configs.player = Player(sdv[0], sdv[1], (player_sprites, all_sprites))
                elif map[lay][pos] == '|':
                    self.doors.append(Door(sdv, (items, collis, doors, all_sprites)))
                elif map[lay][pos] == '&':
                    self.chests.append(Chest(sdv, (items, collis, chests_sprites, all_sprites)))
                elif map[lay][pos] == '!':
                    self.enemies.append(Enemy(sdv[0], sdv[1], (collis, enemy_sprites, all_sprites)))
                elif map[lay][pos] == 'B':
                    self.enemies.append(Boss(sdv[0], sdv[1], (collis, enemy_sprites, all_sprites)))
    def draw(self):
        for obj in self.objects:
            self.screen.blit(obj.image, obj.rect)
        for enemy in self.enemies:
            self.screen.blit(enemy.image, enemy.rect)
        for item in self.items:
            self.screen.blit(item.image, item.rect)
        for chest in self.chests:
            self.screen.blit(chest.image, chest.rect)
        for door in self.doors:
            self.screen.blit(door.image, door.rect)

    def collision(self):
        return collis


def generate_level(screen, all_sprites):
    rooms = sample(range(1, 11), 8)
    for i in range(len(rooms)):
        if i == 0:
            groups.levels.append(Level(f"data/levels/save_levels/start_room.txt", screen, all_sprites))
        if 0 <= i < 4:
            groups.levels.append(Level(f'data/levels/room_{rooms[i]}.txt', screen, all_sprites))
        if i == 4:
            groups.levels.append(Level(f"data/levels/save_levels/chest_room_1.txt", screen, all_sprites))
        if i >= 4:
            groups.levels.append(Level(f'data/levels/room_{rooms[i]}.txt', screen, all_sprites))
        if i == len(rooms) - 1:
            groups.levels.append(Level(f"data/levels/save_levels/chest_room_2.txt", screen, all_sprites))
        

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
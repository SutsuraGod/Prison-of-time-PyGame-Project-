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
from groups import all_sprites, player_sprites, bow_sprites, arrow_sprites

from board import Level

def draw_mask(surface, mask, rect):
        mask_surface = mask.to_surface(setcolor=(255, 0, 0), unsetcolor=(0, 0, 0, 0))
        surface.blit(mask_surface, rect.topleft)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
    pygame.display.set_caption('Prison of Time')
    clock = pygame.time.Clock()
    running = True

    level = Level(r"data\levels\level_46_25.txt", screen, all_sprites)

    player = Player(level, 100, 100, (player_sprites, all_sprites))
    bow = Bow(player.rect.center, (bow_sprites, all_sprites))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Arrow(player.rect.center, event.pos, (arrow_sprites, all_sprites))

        player.moving_event(pygame.key.get_pressed())
        
        screen.fill('grey')
        level.draw()


        player_sprites.draw(screen)
        bow_sprites.draw(screen)
        arrow_sprites.draw(screen)

        player.update(pygame.mouse.get_pos())
        bow.update(player.rect.center, pygame.mouse.get_pos())
        arrow_sprites.update()
        clock.tick(configs.FPS)
        pygame.display.flip()

    pygame.quit()
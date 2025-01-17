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
import groups
from groups import all_sprites, player_sprites, bow_sprites, arrow_sprites, levels, doors
import time


from board import Level, generate_level

# def draw_mask(surface, mask, rect):
#         mask_surface = mask.to_surface(setcolor=(255, 0, 0), unsetcolor=(0, 0, 0, 0))
#         surface.blit(mask_surface, rect.topleft)
def enable_attack():
    global can_attack
    can_attack = True


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
    pygame.display.set_caption('Prison of Time')
    clock = pygame.time.Clock()
    running = True
    ATTACK_EVENT = pygame.USEREVENT + 1
    attack_cooldown = 500
    last_attack_time = 0

    generate_level(screen, all_sprites)
    groups.current_level = levels[0]

    bow = Bow(configs.player.rect.center, (bow_sprites, all_sprites))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # ЛКМ = 1
            #     current_time = pygame.time.get_ticks()
            #     if current_time - last_attack_time >= attack_cooldown:
            #         Arrow(configs.player.rect.center, event.pos, (arrow_sprites, all_sprites))
            #         last_attack_time = current_time
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            current_time = pygame.time.get_ticks()
            if current_time - last_attack_time >= attack_cooldown:
                Arrow(configs.player.rect.center, pygame.mouse.get_pos(), (arrow_sprites, all_sprites))
                last_attack_time = current_time

        keys = pygame.key.get_pressed()

        configs.player.moving_event(keys)

        screen.fill('gray')

        groups.current_level.draw() 
        player_sprites.draw(screen)
        bow_sprites.draw(screen)
        arrow_sprites.draw(screen)

        configs.player.update(pygame.mouse.get_pos())
        bow.update(configs.player.rect.center, pygame.mouse.get_pos())
        arrow_sprites.update()

        clock.tick(configs.FPS)
        pygame.display.flip()

    pygame.quit()
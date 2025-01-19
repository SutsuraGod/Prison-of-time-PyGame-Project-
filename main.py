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
from objects.fireball import Fireball
import groups
from groups import all_sprites, player_sprites, bow_sprites, arrow_sprites, levels, chests_sprites
from groups import spell_sprites
from board import generate_level

# def draw_mask(surface, mask, rect):
#         mask_surface = mask.to_surface(setcolor=(255, 0, 0), unsetcolor=(0, 0, 0, 0))
#         surface.blit(mask_surface, rect.topleft)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
    pygame.display.set_caption('Prison of Time')
    clock = pygame.time.Clock()
    running = True
    ATTACK_EVENT = pygame.USEREVENT + 1
    attack_cooldown = 500
    last_attack_time = 0
    spell_cooldown = 1000
    last_spelling_time = 0

    generate_level(screen, all_sprites)
    groups.current_level = levels[4]

    bow = Bow(configs.player.rect.center, (bow_sprites, all_sprites))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            current_attack_time = pygame.time.get_ticks()
            if current_attack_time - last_attack_time >= attack_cooldown:
                Arrow(filename='arrow.png', spawn_pos=configs.player.rect.center,
                    target_pos=pygame.mouse.get_pos(), normal_angle=45, groups=(arrow_sprites, all_sprites))
                last_attack_time = current_attack_time

        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:
            current_spelling_time = pygame.time.get_ticks()
            if current_spelling_time - last_spelling_time >= spell_cooldown:
                Fireball(filename='fireball.png', spawn_pos=configs.player.rect.center,
                        target_pos=pygame.mouse.get_pos(), normal_angle=270, groups=(spell_sprites, all_sprites))
                last_spelling_time = current_spelling_time

        configs.player.moving_event(keys)

        screen.fill('gray')

        groups.current_level.draw()
        player_sprites.draw(screen)
        bow_sprites.draw(screen)
        arrow_sprites.draw(screen)
        spell_sprites.draw(screen)

        configs.player.update(pygame.mouse.get_pos())
        bow.update(configs.player.rect.center, pygame.mouse.get_pos())
        arrow_sprites.update()
        spell_sprites.update()
        if groups.levels.index(groups.current_level) == 5:
            chests_sprites.update(configs.player.rect.center, keys, screen)

        clock.tick(configs.FPS)
        pygame.display.flip()

    pygame.quit()
import pygame, sys
import configs
import assets
from objects.bow import Bow
from objects.arrow import Arrow
from objects.fireball import Fireball
from objects.icespell import Icespell
import groups
from groups import all_sprites, player_sprites, bow_sprites, arrow_sprites, levels, chests_sprites
from groups import spell_sprites, doors
from board import generate_level
from button import Button


def default_start():
    configs.player = None
    groups.all_sprites.empty()
    groups.player_sprites.empty()
    groups.bow_sprites.empty()
    groups.arrow_sprites.empty()
    groups.items.empty()
    groups.collis.empty()
    groups.doors.empty()
    groups.chests_sprites.empty()
    groups.spell_sprites.empty()
    groups.enemy_sprites.empty()
    groups.items_sprite.empty()
    groups.levels = []
    groups.current_level = []


def print_hp(screen, player):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(f'{player.health}', True, (0, 0, 0))
    screen.blit(text_surface, (50, 50))
    hp_image = assets.load_sprite('hp.png')
    hp_image = pygame.transform.scale2x(hp_image)
    screen.blit(hp_image, (70, 50))


def terminate():
    pygame.quit()
    sys.exit()


def main_menu():
    while True:
        screen.fill('black')
        mouse_pos = pygame.mouse.get_pos()

        menu_text = pygame.font.Font(None, 72).render('MAIN MENU', True, 'White')
        menu_rect = menu_text.get_rect(center=(500, 140))

        play_button = Button(pos=(500, 420), text_input='PLAY', font=pygame.font.Font(None, 72),
                            base_color='White', alt_color='Green')
        quit_button = Button(pos=(500, 700), text_input='QUIT', font=pygame.font.Font(None, 72),
                            base_color='White', alt_color='Green')
        
        screen.blit(menu_text, menu_rect)
        
        for button in [play_button, quit_button]:
            button.change_color(mouse_pos)
            button.update(screen=screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(mouse_pos):
                    play()
                if quit_button.check_for_input(mouse_pos):
                    terminate()
        pygame.display.flip()


def play():
    default_start()
    attack_cooldown = 500
    last_attack_time = 0
    spell_cooldown = 1500
    last_spelling_time = 0
    generate_level(screen, all_sprites)
    groups.current_level = groups.levels[0]

    bow = Bow(configs.player.rect.center, (bow_sprites, all_sprites))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

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
                if configs.player.current_spell == 'fireball':
                    Fireball(filename='fireball.png', spawn_pos=configs.player.rect.center,
                            target_pos=pygame.mouse.get_pos(), normal_angle=270, groups=(spell_sprites, all_sprites))
                if configs.player.current_spell == 'icespell':
                    Icespell(filename='icespell.png', spawn_pos=configs.player.rect.center,
                            target_pos=pygame.mouse.get_pos(), normal_angle=0, groups=(spell_sprites, all_sprites))

                last_spelling_time = current_spelling_time

        configs.player.moving_event(keys)

        screen.fill('gray')

        groups.current_level.draw()
        player_sprites.draw(screen)
        bow_sprites.draw(screen)
        arrow_sprites.draw(screen)
        spell_sprites.draw(screen)
        print_hp(screen, configs.player)

        if not groups.current_level.enemies:
            configs.fight = False
        else:
            configs.fight = True
            
        for i in range(last_len := len(groups.current_level.enemies)):
                enemy = groups.current_level.enemies[i]
                enemy.move(configs.player, configs.player.rect, groups.current_level.objects, configs.player.rect.center)
                if last_len != len(groups.current_level.enemies):
                    break
                groups.current_level.enemies[i] = enemy

        configs.player.update(pygame.mouse.get_pos())
        bow.update(configs.player.rect.center, pygame.mouse.get_pos())
        arrow_sprites.update()
        spell_sprites.update()
        doors.update(configs.fight)
        if groups.levels.index(groups.current_level) == 5:
            chests_sprites.update(configs.player.rect.center, keys, screen)
        
        clock.tick(configs.FPS)
        pygame.display.flip()

        if configs.player.health <= 0:
            main_menu()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
    pygame.display.set_caption('Prison of Time')
    clock = pygame.time.Clock()
    ATTACK_EVENT = pygame.USEREVENT + 1
    main_menu()

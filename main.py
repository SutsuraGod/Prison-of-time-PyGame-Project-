import pygame, sys
import configs
import assets
from objects.bow import Bow
from objects.arrow import Arrow
from objects.fireball import Fireball
from objects.icespell import Icespell
from objects.bullet import Bullet
import groups
from groups import all_sprites, player_sprites, bow_sprites, arrow_sprites, levels, chests_sprites
from groups import spell_sprites, enemy_sprites, collis, doors
from board import generate_level
from button import Button
from sound_manager import play_sound, stop_sound, is_sound_playing


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
    play_sound('menu')
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
                    stop_sound('menu')
                    play_sound('click')
                    play()
                if quit_button.check_for_input(mouse_pos):
                    stop_sound('menu')
                    play_sound('click')
                    while is_sound_playing('click'):
                        pygame.time.wait(10)
                    terminate()
        pygame.display.flip()


def pause_menu():
    play_sound('menu')
    running = True
    while running:
        screen.fill('black')
        mouse_pos = pygame.mouse.get_pos()

        pause_text = pygame.font.Font(None, 72).render('PAUSE', True, 'White')
        pause_rect = pause_text.get_rect(center=(500, 105))

        resume_button = Button(pos=(500, 315), text_input='RESUME', font=pygame.font.Font(None, 72),
                            base_color="White", alt_color='Green')
        main_menu_button = Button(pos=(500, 525), text_input='MAIN MENU', font=pygame.font.Font(None, 72),
                            base_color='White', alt_color='Green')
        quit_button = Button(pos=(500, 735), text_input='QUIT', font=pygame.font.Font(None, 72),
                            base_color='White', alt_color='Green')

        screen.blit(pause_text, pause_rect)

        for button in [resume_button, main_menu_button, quit_button]:
            button.change_color(mouse_pos)
            button.update(screen=screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resume_button.check_for_input(mouse_pos):
                    stop_sound('menu')
                    play_sound('click')
                    while is_sound_playing('click'):
                        pygame.time.wait(10)
                    current_time = pygame.time.get_ticks()
                    configs.player.last_attack_time = current_time
                    configs.player.last_spelling_time = current_time
                    running = False
                elif main_menu_button.check_for_input(mouse_pos):
                    stop_sound('menu')
                    play_sound('click')
                    while is_sound_playing('click'):
                        pygame.time.wait(10)
                    main_menu()
                if quit_button.check_for_input(mouse_pos):
                    stop_sound('menu')
                    play_sound('click')
                    while is_sound_playing('click'):
                        pygame.time.wait(10)
                    terminate()

        pygame.display.flip()


def play():
    play_sound('in game')
    default_start()
    generate_level(screen, all_sprites)
    groups.current_level = groups.levels[0]
    bow = Bow(configs.player.rect.center, (bow_sprites, all_sprites))

    attack_cooldown = 500
    spell_cooldown = 1500

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                stop_sound('in game')
                pause_menu()
                play_sound('in game')
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            current_attack_time = pygame.time.get_ticks()
            if current_attack_time - configs.player.last_attack_time >= attack_cooldown:
                Arrow(filename='arrow.png', spawn_pos=configs.player.rect.center,
                    target_pos=pygame.mouse.get_pos(), normal_angle=45, groups=(arrow_sprites, all_sprites))
                play_sound('bow')
                configs.player.last_attack_time = current_attack_time

        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:
            current_spelling_time = pygame.time.get_ticks()
            if current_spelling_time - configs.player.last_spelling_time >= spell_cooldown:
                if configs.player.current_spell == 'fireball':
                    Fireball(filename='fireball.png', spawn_pos=configs.player.rect.center,
                            target_pos=pygame.mouse.get_pos(), normal_angle=270, groups=(spell_sprites, all_sprites))
                    play_sound('spell')
                if configs.player.current_spell == 'icespell':
                    Icespell(filename='icespell.png', spawn_pos=configs.player.rect.center,
                            target_pos=pygame.mouse.get_pos(), normal_angle=0, groups=(spell_sprites, all_sprites))
                    play_sound('spell')
                configs.player.last_spelling_time = current_spelling_time
                    
        configs.player.moving_event(keys)

        screen.fill('gray')

        groups.current_level.draw()
        player_sprites.draw(screen)
        bow_sprites.draw(screen)
        arrow_sprites.draw(screen)
        spell_sprites.draw(screen)

        for bullet in groups.all_sprites:
            if isinstance(bullet, Bullet):
                bullet.update(configs.player)  # Обновляем пулю
                bullet.draw(screen)  # Отрисовываем пулю вручную

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
        if groups.levels.index(groups.current_level) % 5 == 0:
            for i in groups.current_level.chests:
                i.update(configs.player.rect.center, keys, screen)
        
        clock.tick(configs.FPS)
        pygame.display.flip()

        if configs.player.health <= 0:
            stop_sound('in game')
            main_menu()

        if not configs.player.playing:
            game_over()


def game_over():
    play_sound('menu')
    while True:
        screen.fill('black')
        mouse_pos = pygame.mouse.get_pos()

        game_over_text = pygame.font.Font(None, 72).render('GAME OVER', True, 'White')
        game_over_rect = game_over_text.get_rect(center=(500, 140))
        you_win_text = pygame.font.Font(None, 72).render('You win!', True, 'White')
        you_win_rect = you_win_text.get_rect(center=(500, 200))

        main_menu_button = Button(pos=(500, 420), text_input='MAIN MENU', font=pygame.font.Font(None, 72),
                            base_color='White', alt_color='Green')
        quit_button = Button(pos=(500, 700), text_input='QUIT', font=pygame.font.Font(None, 72),
                            base_color='White', alt_color='Green')
        
        screen.blit(game_over_text, game_over_rect)
        screen.blit(you_win_text, you_win_rect)
        
        for button in [main_menu_button, quit_button]:
            button.change_color(mouse_pos)
            button.update(screen=screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.check_for_input(mouse_pos):
                    stop_sound('menu')
                    play_sound('click')
                    main_menu()
                if quit_button.check_for_input(mouse_pos):
                    stop_sound('menu')
                    play_sound('click')
                    while is_sound_playing('click'):
                        pygame.time.wait(10)
                    terminate()
        pygame.display.flip()



if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
    pygame.display.set_caption('Prison of Time')
    clock = pygame.time.Clock()
    ATTACK_EVENT = pygame.USEREVENT + 1
    main_menu()
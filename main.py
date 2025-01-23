import pygame
import configs
import assets
from objects.bow import Bow
from objects.arrow import Arrow
from objects.fireball import Fireball
from objects.icespell import Icespell
import groups
from groups import all_sprites, player_sprites, bow_sprites, arrow_sprites, levels, chests_sprites
from groups import spell_sprites, enemy_sprites, collis, doors
from board import generate_level


def print_hp(screen, player):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(f'{player.health}', True, (0, 0, 0))
    screen.blit(text_surface, (50, 50))
    hp_image = assets.load_sprite('hp.png')
    hp_image = pygame.transform.scale2x(hp_image)
    screen.blit(hp_image, (70, 50))


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
    pygame.display.set_caption('Prison of Time')
    clock = pygame.time.Clock()
    running = True
    ATTACK_EVENT = pygame.USEREVENT + 1
    attack_cooldown = 500
    last_attack_time = 0
    spell_cooldown = 1500
    last_spelling_time = 0

    generate_level(screen, all_sprites)
    groups.current_level = levels[0]

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
        
        if configs.player.health <= 0:
            pygame.quit()

        clock.tick(configs.FPS)
        pygame.display.flip()

    pygame.quit()
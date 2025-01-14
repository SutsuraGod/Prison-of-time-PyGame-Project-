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


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
    pygame.display.set_caption('Prison of Time')
    clock = pygame.time.Clock()
    running = True

    all_sprites = pygame.sprite.Group()
    player_sprites = pygame.sprite.Group()
    bow_sprites = pygame.sprite.Group()
    arrow_sprites = pygame.sprite.Group()

    player = Player((player_sprites, all_sprites))
    bow = Bow(player.rect.center, (bow_sprites, all_sprites))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Arrow(player.rect.center, event.pos, (arrow_sprites, all_sprites))

        player.moving_event(pygame.key.get_pressed())
        
        screen.fill('pink')
        player_sprites.draw(screen)
        bow_sprites.draw(screen)
        arrow_sprites.draw(screen)

        player.update(pygame.mouse.get_pos())
        bow.update(player.rect.center, pygame.mouse.get_pos())
        arrow_sprites.update()
        clock.tick(configs.FPS)
        pygame.display.flip()
        print(len(arrow_sprites))
    pygame.quit()
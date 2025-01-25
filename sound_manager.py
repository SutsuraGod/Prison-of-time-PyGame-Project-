import pygame


pygame.mixer.init()

music_path = 'data/music/'
menu_music = pygame.mixer.Sound(f'{music_path}menu_music.wav')
menu_music.set_volume(0.3)
in_game_music = pygame.mixer.Sound(f'{music_path}in_game_music.wav')
in_game_music.set_volume(0.2)
click_sound = pygame.mixer.Sound(f'{music_path}click_sound.wav')
bow_sound = pygame.mixer.Sound(f'{music_path}shoot_bow.ogg')
bow_sound.set_volume(0.5)
spell_sound = pygame.mixer.Sound(f'{music_path}shoot_spell.wav')
raising_item_sound = pygame.mixer.Sound(f'{music_path}raising_item.wav')
raising_item_sound.set_volume(0.3)

soundtrack_channel = pygame.mixer.Channel(0)
click_sound_channel = pygame.mixer.Channel(1)
spell_sound_channel = pygame.mixer.Channel(2)
bow_sound_channel = pygame.mixer.Channel(3)
raising_item_sound_channel = pygame.mixer.Channel(4)


def play_sound(sound):
    '''Воспроизводит музыку или звук'''
    if sound == 'menu':
        soundtrack_channel.play(menu_music, loops=-1)
    elif sound == 'in game':
        soundtrack_channel.play(in_game_music, loops=-1)
    elif sound == 'click':
        click_sound_channel.play(click_sound)
    elif sound == 'spell':
        spell_sound_channel.play(spell_sound)
    elif sound == 'bow':
        bow_sound_channel.play(bow_sound)
    elif sound == 'item':
        raising_item_sound_channel.play(raising_item_sound)


def stop_sound(sound):
    '''Останавливает музыку или звук'''
    if sound == 'menu':
        soundtrack_channel.stop()
    elif sound == 'in game':
        soundtrack_channel.stop()
    elif sound == 'click':
        click_sound_channel.stop()
    elif sound == 'spell':
        spell_sound_channel.stop()
    elif sound == 'bow':
        bow_sound_channel.stop()
    elif sound == 'item':
        raising_item_sound_channel.stop()


def is_sound_playing(sound):
    '''Проверяет, проигрывается ли звук или музыка'''
    if sound == 'menu':
        return soundtrack_channel.get_busy()
    elif sound == 'in game':
        return soundtrack_channel.get_busy()
    elif sound == 'click':
        return click_sound_channel.get_busy()
    elif sound == 'spell':
        return spell_sound_channel.get_busy()
    elif sound == 'bow':
        return bow_sound_channel.get_busy()
    elif sound == 'item':
        return raising_item_sound_channel.get_busy()
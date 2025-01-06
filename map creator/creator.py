import pygame


level_name = input()
pygame.init()
SIZE = WIDTH, HEIGHT = 1000, 840
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Редактор уровней')
clock = pygame.time.Clock()
FPS = 60
objects = {
    'wall':'#',
    'player':'@',
    'enemy':'!',
    'void':'.',
    'barrier':'%',
    'door':'|',
    'chest':'&'
}
player_pos = (-1, -1)


class Board():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [['.'] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 40
    
    def render(self, screen):
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == '#': # если стена
                    color = (50, 50, 50)
                elif self.board[row][col] == '@': # если игрок
                    color = (0, 255, 0)
                elif self.board[row][col] == '.': # если пустота
                    color = (0, 0, 0)
                elif self.board[row][col] == '!': # если враг
                    color = (255, 0, 0)
                elif self.board[row][col] == '%': # если какое-то препятствие
                    color = (128, 64, 48)
                elif self.board[row][col] == '|': # если дверь
                    color = (0, 0, 255)
                elif self.board[row][col] == '&': # если сундук
                    color = (255, 0, 255)

                pygame.draw.rect(
                    screen,
                    color,
                    (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                )

                pygame.draw.rect(
                    screen,
                    (200, 200, 200),
                    (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size),
                    1
                )

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= x <= self.width - 1 and 0 <= y <= self.height - 1:
            return y, x
        return None

    def on_click(self, cell_coords, obj):
        if cell_coords:
            row, col = cell_coords
            global player_pos
            if obj != 'player':
                self.board[row][col] = objects[obj]
            else:
                if player_pos == (-1, -1):
                    self.board[row][col] = objects[obj]
                    player_pos = row, col
                else:
                    self.board[player_pos[0]][player_pos[1]] = '.'
                    self.board[row][col] = objects[obj]
                    player_pos = row, col
        else:
            pass

    def get_click(self, mouse_pos, obj):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell, obj)


def main():
    running = True
    board = Board(25, 21)
    brush = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    with open(f'data/levels/{level_name}', 'w', encoding='utf-8') as file:
                        for row in board.board:
                            file.write(''.join(row) + '\n')

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    brush = 'player'
                elif event.key == pygame.K_2:
                    brush = 'wall'
                elif event.key == pygame.K_3:
                    brush = 'barrier'
                elif event.key == pygame.K_4:
                    brush = 'enemy'
                elif event.key == pygame.K_5:
                    brush = 'door'
                elif event.key == pygame.K_6:
                    brush = 'chest'
                elif event.key == pygame.K_7:
                    brush = 'void'
                print(f'Режим: {brush}')

            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0]:
                if brush:
                    mouse_pos = event.pos
                    board.get_click(mouse_pos, brush)
                else:
                    print('Кисть не выбрана')

        screen.fill('black')
        board.render(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
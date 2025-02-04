class Button():
    def __init__(self, pos, text_input, font, base_color, alt_color):
        self.x, self.y = pos
        self.font = font
        self.base_color, self.alt_color = base_color, alt_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.image = self.text
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text_rect = self.text.get_rect(center=(self.x, self.y))
        
    def update(self, screen):
        '''Отрисовка кнопки'''
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        '''Проверка на нажатие'''
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def change_color(self, position):
        '''Изменение цвета кнопки при наведении на нее курсора'''
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.alt_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
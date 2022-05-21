import pygame, os
from settings import Settings


class Cursor():
    def __init__(self, filename):
        self.rect = None
        self.image = None
        self.action = "hand"
        self.pos = (0, 0)
        pygame.mouse.set_visible(False)
        self.update_sprite(filename)

    def update(self):
        self.pos = pygame.mouse.get_pos()
        self.set_pos(*self.pos)

    def set_pos(self, x, y):
        self.rect.x, self.rect.y = x, y

    def update_sprite(self, filename):
        self.image = pygame.image.load(os.path.join(Settings.path_cursors, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, Settings.cursor_size)
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def get_pressed(self, buttons):
        if pygame.mouse.get_pressed(num_buttons=3) == buttons:
            return True

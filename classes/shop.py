import pygame, os
from settings import Settings


class ShopItem():
    def __init__(self, name, item, amount, price, status):
        self.rect = None
        self.image = None
        self.name = name
        self.item = item
        self.amount = amount
        self.price = price
        self.status = status

    def update_sprite(self, filename):
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (
            int(Settings.window_width * self.game.zoom),
            int(Settings.window_height * self.game.zoom)
        ))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass


class Shop():
    def __init__(self, name, items):
        self.name = name
        self.items = items

    def update(self):
        pass

    def draw(self):
        pass

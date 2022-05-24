import pygame, os
from settings import Settings


class ShopItem():
    def __init__(self, game, size, name, item, amount, price, status):
        self.rect = None
        self.image = None
        self.game = game
        self.size = size
        self.name = name
        self.item = item
        self.amount = amount
        self.price = price
        self.status = status

        self.update_sprite(item.image)

    def update_sprite(self, filename):
        self.image = pygame.image.load(os.path.join(Settings.path_crops, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (
            int(self.size[0] * self.game.zoom),
            int(self.size[1] * self.game.zoom)
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

    def draw(self, screen):
        for item in self.items:
            item.draw(screen)

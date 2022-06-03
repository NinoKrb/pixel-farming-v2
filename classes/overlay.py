import pygame, os
from settings import Settings


class OverlaySprite(pygame.sprite.Sprite):
    def __init__(self, filename, pos, size, path):
        super().__init__()
        self.filename = filename
        self.pos = pos
        self.size = size
        self.path = path
        self.update_sprite(self.filename)

    def update_sprite(self, filename, path=None):
        if path is None:
            path = self.path
        self.image = pygame.image.load(os.path.join(path, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.set_pos(*self.pos)

    def set_pos(self, x, y):
        self.rect.left = x
        self.rect.top = y
        self.pos = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class OverlayManager():
    def __init__(self, game):
        self.amount_label = None
        self.seed_label = None
        self.money_label = None
        self.sprites = pygame.sprite.Group()
        self.game = game

        self.sprites.add(OverlaySprite('slot.png', (16, Settings.window_height - 80), (64, 64), Settings.path_image))
        self.sprites.add(OverlaySprite('label.png', (Settings.window_width - 16 - 105, 16), (105, 39), Settings.path_image))

        self.current_action_item = OverlaySprite('hand_open_02.png', (24, Settings.window_height - 72), (48, 48), Settings.path_cursors)

    def draw(self, screen):
        self.sprites.draw(screen)
        self.current_action_item.draw(screen)

        self.money_label = self.game.inventory_font.render(f"{self.game.money}c", True, (255, 255, 255))
        screen.blit(self.money_label, (Settings.window_width - 110, 26))

        if self.game.action['name'] == "seed":
            self.seed_label = self.game.inventory_font_big.render(f"{self.game.inventory.find_item(self.game.current_seed['item_id']).item.name}", True, (255, 255, 255))
            screen.blit(self.seed_label, (self.current_action_item.rect.right + 25, self.current_action_item.rect.top))

            self.amount_label = self.game.inventory_font.render(f"{self.game.inventory.get_amount_by_id(self.game.current_seed['item_id'])}", True, (255, 255, 255))
            screen.blit(self.amount_label, (self.current_action_item.rect.right + 25, self.current_action_item.rect.top + self.seed_label.get_rect().height + 5))

    def update(self):
        pass

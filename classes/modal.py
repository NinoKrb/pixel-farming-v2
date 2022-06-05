import pygame
import os
from settings import Settings


class ModalSprite(pygame.sprite.Sprite):
    def __init__(self, game, filename, pos, size, path):
        super().__init__()
        self.game = game
        self.filename = filename
        self.pos = pos
        self.size = size
        self.path = path
        self.update_sprite(self.filename)

    def update_sprite(self, filename):
        self.image = pygame.image.load(os.path.join(self.path, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.set_pos(*self.pos)

    def set_pos(self, x, y):
        self.rect.left = x
        self.rect.top = y
        self.pos = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Modal():
    def __init__(self, game):
        self.button_left_label = None
        self.button_right_label = None
        self.title_label = None
        self.text_label = None
        self.game = game
        self.visible = False
        self.container = ModalSprite(self.game, "modal_container.png", (Settings.window_width // 2 - 216, 100), (432, 250), Settings.path_image)
        self.text = ["Bist du dir sicher dass du dieses", " Feld kaufen moechtest"]
        self.title = "Feld Kaufen"
        self.button_left = "Abbrechen"
        self.button_right = "Kaufen"

        self.text_group = []
        for line in self.text:
            self.text_group.append(self.game.inventory_font.render(f"{line}", True, (255, 255, 255)))

    def draw(self, screen):
        if self.visible:
            self.container.draw(screen)

            self.title_label = self.game.inventory_font.render(f"{self.title}", True, (255, 255, 255))
            screen.blit(self.title_label, (self.container.pos[0] + self.container.size[0] // 2 - self.title_label.get_rect().width // 2, self.container.pos[1] + 20))

            line_index = 0
            for line in self.text_group:
                screen.blit(line, (self.container.pos[0] + self.container.size[0] // 2 - line.get_rect().width // 2, self.container.pos[1] + 60 + (line_index * (line.get_rect().height + 5))))
                line_index += 1

            self.button_left_label = ModalSprite(self.game, "cancel.png", (self.container.pos[0] + 130 // 2, self.container.pos[1] + self.container.size[1] - 35), (130, 15), Settings.path_texts)
            self.button_left_label.draw(screen)

            self.button_right_label = ModalSprite(self.game, "buy.png", ((self.container.pos[0] + 150 // 2) + self.container.size[0] // 2, self.container.pos[1] + self.container.size[1] - 35), (90, 15), Settings.path_texts)
            self.button_right_label.draw(screen)

    def update(self):
        pass

    def check_button_collision(self):
        pass

    def check_cursor_position(self, surface):
        if pygame.Rect.collidepoint(surface, *self.game.cursor.pos):
            return True
        return False


class BuyFieldModal(Modal):
    def __init__(self, game, field):
        super().__init__(game)
        self.field = field

    def update(self):
        self.check_button_collision()

    def check_button_collision(self):
        if self.visible:
            if self.game.cursor.get_pressed((1, 0, 0)):
                try:
                    if self.check_cursor_position(self.button_right_label.rect):
                        if Settings.field_prices[self.field] <= self.game.money:
                            if not self.field in self.game.owned_fields:
                                self.game.money -= Settings.field_prices[self.field]
                                self.game.owned_fields.append(self.field)
                                self.game.field_manager.buy_field(self.field)
                                self.visible = False

                    if self.check_cursor_position(self.button_left_label.rect):
                        self.visible = False
                except:
                    pass

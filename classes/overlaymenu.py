import os, pygame
from settings import Settings
from classes.timer import Timer


class OverlaySprite(pygame.sprite.Sprite):
    def __init__(self, filename, pos, size, path):
        super().__init__()
        self.filename = filename
        self.pos = pos
        self.size = size
        self.path = path
        self.update_sprite(self.filename, self.pos, self.size)

    def update_sprite(self, filename, pos, size):
        self.image = pygame.image.load(os.path.join(self.path, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.set_pos(*pos)

    def set_pos(self, x, y):
        self.rect.left = x
        self.rect.top = y
        self.pos = (x, y)

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class OverlayButton(OverlaySprite):
    def __init__(self, game, method, filename, pos, size, path):
        super().__init__(filename, pos, size, path)
        self.game = game
        self.method = method
        self.click_timer = Timer(500)

    def update(self):
        if self.check_cursor_position(self.rect):
            if self.game.cursor.get_pressed((1, 0, 0)):
                if self.click_timer.is_next_stop_reached():
                    eval(self.method)

    def check_cursor_position(self, surface):
        if pygame.Rect.collidepoint(surface, *self.game.cursor.pos):
            return True
        return False


class Overlay():
    def __init__(self, color, size, pos, alpha):
        self.color = color
        self.size = size
        self.pos = pos
        self.alpha = alpha

        self.surface = pygame.surface.Surface(self.size)
        self.surface.fill(self.color)
        self.surface.set_alpha(self.alpha)
        self.rect = self.surface.get_rect()

    def draw(self, screen):
        screen.blit(self.surface, self.rect)

    def update(self):
        pass


class OverlayText():
    def __init__(self, text, pos, color, font):
        self.image = None
        self.text = text
        self.pos = pos
        self.font = font
        self.color = color

    def draw(self, screen):
        self.image = self.font.render(f"{self.text}", True, self.color)
        screen.blit(self.image, self.pos)

    def update(self):
        pass


class OverlayMenu():
    def __init__(self, game):
        self.game = game
        self.sprites = []

    def run(self):
        self.update()
        self.draw(self.game.screen)

    def draw(self, screen):
        for sprite in self.sprites:
            sprite.draw(screen)

    def update(self):
        for sprite in self.sprites:
            sprite.update()


class PauseMenu(OverlayMenu):
    def __init__(self, game):
        super().__init__(game)
        self.sprites.append(Overlay((0, 0, 0), (Settings.window_width, Settings.window_height), (0, 0), 100))
        self.sprites.append(OverlayText("Pause", (Settings.window_width // 2 - 50, 150), (255, 255, 255), self.game.inventory_font_big))

        self.sprites.append(OverlayButton(self.game, "self.game.pause_menu.close_menu()", "play_button.png", (Settings.window_width // 2 - 100, 250), (200, 50), Settings.path_image))
        self.sprites.append(OverlayButton(self.game, "self.game.save_game_manager.save_storage()", "save_button.png", (Settings.window_width // 2 - 100, 325), (200, 50), Settings.path_image))
        self.sprites.append(OverlayButton(self.game, "self.game.music_player.toggle_sounds()", "music_on_button.png", (Settings.window_width // 2 - 100, 400), (200, 50), Settings.path_image))
        self.sprites.append(OverlayButton(self.game, "self.game.quit()", "quit_button.png", (Settings.window_width // 2 - 100, 475), (200, 50), Settings.path_image))

    def close_menu(self):
        self.game.pause_state = False

    def update(self):
        for sprite in self.sprites:
            sprite.update()

            try:
                if sprite.method == "self.game.music_player.toggle_sounds()":
                    if self.game.music_player.muted:
                        sprite.update_sprite("music_off_button.png", sprite.pos, sprite.size)
                    else:
                        sprite.update_sprite("music_on_button.png", sprite.pos, sprite.size)
            except:
                pass


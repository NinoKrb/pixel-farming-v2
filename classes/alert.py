import pygame
from settings import Settings
from classes.timer import Timer


class Alert():
    def __init__(self, game, text, color):
        self.image = None
        self.game = game
        self.text = text
        self.color = color
        self.pos = Settings.alert_pos
        self.font = self.game.inventory_font
        self.timer = Timer(Settings.alert_duration, False)

    def draw(self, screen, offset):
        self.image = self.font.render(f"{self.text}", True, self.color)
        self.image.set_alpha(self.timer.next - pygame.time.get_ticks())
        screen.blit(self.image, (self.pos[0], self.pos[1] + offset))


class AlertManager():
    def __init__(self, game):
        self.game = game
        self.alerts = []

    def create_alert(self, text, color=Settings.alert_color):
        self.alerts.append(Alert(self.game, text, color))

    def draw(self, screen):
        index = 0
        for alert in reversed(self.alerts):
            alert.draw(screen, 15 * index)
            index += 1

    def update(self):
        for alert in self.alerts:
            if alert.timer.is_next_stop_reached():
                self.alerts.remove(alert)

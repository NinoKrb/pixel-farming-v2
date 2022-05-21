from classes.action import Action
from classes.animation_set import AnimationSet
from classes.animation import Animation
from classes.timer import Timer
from settings import Settings
import pygame, os


class Character(pygame.sprite.Sprite):
    def __init__(self, options, size, pos):
        self.surface = pygame.Surface(size)
        self.options = options
        self.size = size
        self.pos = pos
        self.flip = False

        animation_path = os.path.join(Settings.path_image, 'sprites', 'character')
        animations = [
            Animation('WALKING', animation_path, self.options, (64, 64), 16, 50),
            Animation('DIG', animation_path, self.options, (64, 64), 16, 50),
            Animation('CAUGHT', animation_path, self.options, (64, 64), 16, 50),
            Animation('REELING', animation_path, self.options, (64, 64), 16, 50),
            Animation('WAITING', animation_path, self.options, (64, 64), 16, 50),
            Animation('CASTING', animation_path, self.options, (64, 64), 16, 50),
            Animation('HAMMERING', animation_path, self.options, (64, 64), 16, 50),
            Animation('SWIMMING', animation_path, self.options, (64, 64), 16, 50),
            Animation('MINING', animation_path, self.options, (64, 64), 16, 50),
            Animation('AXE', animation_path, self.options, (64, 64), 16, 50),
            Animation('ROLL', animation_path, self.options, (64, 64), 16, 50),
            Animation('JUMP', animation_path, self.options, (64, 64), 16, 50),
            Animation('RUN', animation_path, self.options, (64, 64), 16, 50),
            Animation('DOING', animation_path, self.options, (64, 64), 16, 50),
            Animation('DEATH', animation_path, self.options, (64, 64), 16, 50),
            Animation('HURT', animation_path, self.options, (64, 64), 16, 50),
            Animation('WATERING', animation_path, self.options, (64, 64), 16, 50),
            Animation('CARRY', animation_path, self.options, (64, 64), 16, 50),
            Animation('IDLE', animation_path, self.options, (64, 64), 16, 50),
            Animation('ATTACK', animation_path, self.options, (64, 64), 16, 50)
        ]

        self.animation_set = AnimationSet('character', animations)
        self.action_handler = Action({'name': 'IDLE', 'loop': True})

        self.update_sprite(self.surface)
        self.set_position(*self.pos)

    def update_sprite(self, surface):
        self.image = pygame.transform.scale(surface, self.size)
        if self.flip:
            self.image = pygame.transform.flip(self.image, self.flip, False)
        self.rect = self.image.get_rect()

    def set_position(self, x, y):
        self.rect.x, self.rect.y = x, y

    def update(self):
        frame = self.animation_set.process_animation(self.action_handler.current_action['name'])
        if frame:
            self.update_sprite(frame)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

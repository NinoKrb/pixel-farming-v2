import pygame, os, csv, json, random
from settings import Settings
from classes.player import Character
from classes.timer import Timer
from classes.fields import *

class ImageLayer(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class CollisionLayer(ImageLayer):
    def __init__(self, filename):
        super().__init__(filename)

class Cursor():
    def __init__(self, filename):
        self.action = "hand"
        self.pos = (0,0)
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


class Game():
    def __init__(self):
        super().__init__()
        pygame.init()   
        pygame.display.set_caption(Settings.title)

        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()
        self.background = ImageLayer("floor.png")
        self.collision_layer = CollisionLayer("collision.png")

        self.cursor = Cursor(Settings.cursors['default'])

        self.field_manager = FieldManager(self)

        # self.character = Character(options={ 
        #    'base': "base", 
        #    'haircut': "curlyhair", 
        #    'tools': "tools"
        # }, size=Settings.player_size, pos=(0,0))

        self.running = True 

    def run(self):
        while self.running:
            self.clock.tick(Settings.fps)
            self.draw()
            self.update()
            self.watch_for_events()
    
    def update(self):
        self.field_manager.update()
        self.cursor.update()
        # self.character.update()

    def draw(self):
        self.background.draw(self.screen)
        self.collision_layer.draw(self.screen)
        self.field_manager.draw_fields(self.screen)
        self.cursor.draw(self.screen)
        # self.character.draw(self.screen)
        pygame.display.flip()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            if event.type == pygame.QUIT:
                self.running = False
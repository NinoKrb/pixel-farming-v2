import pygame, os
from settings import Settings
from classes.player import Character
from classes.timer import Timer
from classes.cursor import Cursor
from classes.fields import FieldManager
from classes.item import ItemManager
from classes.inventory import InventoryHandler, InventoryManager

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

class Game():
    def __init__(self):
        super().__init__()
        pygame.init()   
        pygame.display.set_caption(Settings.title)

        self.inventory_font = pygame.font.SysFont("arial", 14)

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

        self.item_manager = ItemManager()

        self.inventory = InventoryHandler()
        self.inventory.initialize_itemstacks(self.item_manager.items)

        self.inventory_manager = InventoryManager(self)
        self.inventory_manager.init_itemstacks(self.inventory.items)

        self.inventory_state = False

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
        if self.inventory_state:
            self.inventory_manager.draw(self.screen)
        self.cursor.draw(self.screen)
        # self.character.draw(self.screen)
        pygame.display.flip()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if event.key == pygame.K_e:
                    self.inventory_state = not self.inventory_state

            if event.type == pygame.QUIT:
                self.running = False
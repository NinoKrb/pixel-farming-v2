import pygame, os
from settings import Settings
from classes.cursor import Cursor
from classes.fields import FieldManager
from classes.item import ItemManager
from classes.inventory import InventoryHandler, InventoryManager
from classes.shop import ShopManager, ShopItem


class ImageLayer(pygame.sprite.Sprite):
    def __init__(self, game, filename):
        super().__init__()
        self.game = game
        self.original_image = self.update_sprite(filename).copy()

    def update_sprite(self, filename):
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.update_zoom(self.image)
        return self.image

    def update_zoom(self, image):
        self.image = pygame.transform.scale(image, (
            int(Settings.window_width * self.game.zoom),
            int(Settings.window_height * self.game.zoom)
        ))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class CollisionLayer(ImageLayer):
    def __init__(self, game, filename):
        super().__init__(game, filename)


class Game():
    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.display.set_caption(Settings.title)

        self.money = 0

        self.zoom = Settings.zoom_default
        self.inventory_font = pygame.font.Font(os.path.join(Settings.path_font, "8-BIT WONDER.TTF"), 14)

        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()

        self.background = ImageLayer(self, "floor.png")
        self.collision_layer = CollisionLayer(self, "collision.png")

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

        self.inventory_manager = InventoryManager(self, 'inv_container.png', 'slot.png')
        self.inventory_manager.init_itemstacks(self.inventory.items)

        shop_items = [
            ShopItem(self.item_manager.get_item_by_id(13), 25, "buy"),
            ShopItem(self.item_manager.get_item_by_id(14), 25, "buy"),
            ShopItem(self.item_manager.get_item_by_id(2), 25, "sell")
        ]
        self.shop_manager = ShopManager(self, 'inv_container.png', 'slot.png')
        self.shop_manager.init_itemstacks(shop_items)

        self.inventory_state = False
        self.shop_state = False
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
        elif self.shop_state:
            self.shop_manager.draw(self.screen)
        self.cursor.draw(self.screen)
        # self.character.draw(self.screen)
        pygame.display.flip()

    def update_zoom(self):
        self.background.update_zoom(self.background.original_image)
        self.collision_layer.update_zoom(self.collision_layer.original_image)
        self.field_manager.update_zoom()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if event.key == pygame.K_e:
                    if not self.shop_state:
                        self.inventory_state = not self.inventory_state

                if event.key == pygame.K_s:
                    if not self.inventory_state:
                        self.shop_state = not self.shop_state

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.shop_state:
                    self.shop_manager.check_cursor()

            if event.type == pygame.MOUSEWHEEL:
                # Zoom in
                if event.y == 1:
                    new_zoom = round(self.zoom + Settings.zoom_step, 1)

                # Zoom Out
                else:
                    new_zoom = round(self.zoom - Settings.zoom_step, 1)

                if Settings.zoom_max >= new_zoom >= Settings.zoom_min:
                    self.zoom = new_zoom
                    self.update_zoom()

import random

import pygame, os
from settings import Settings
from classes.cursor import Cursor
from classes.fields import FieldManager
from classes.item import ItemManager
from classes.inventory import InventoryHandler, InventoryManager
from classes.shop import ShopManager, ShopItem
from classes.overlay import OverlayManager
from classes.player import Character, WalkingNPC
from classes.map import Map
from classes.storage import Storage


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
        self.mask = pygame.mask.from_surface(self.image)


class Game():
    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.display.set_caption(Settings.title)

        self.save_game_manager = Storage(self)

        self.money = self.save_game_manager.storage['money']
        self.owned_fields = self.save_game_manager.storage['owned_fields']
        self.characters = pygame.sprite.Group()
        self.modals = []

        self.zoom = Settings.zoom_default
        self.inventory_font = pygame.font.Font(os.path.join(Settings.path_font, "8-BIT WONDER.TTF"), 14)

        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()

        self.background = ImageLayer(self, "floor.png")
        self.collision_layer = CollisionLayer(self, "collision.png")

        self.cursor = Cursor(Settings.cursors['default'])

        self.field_manager = FieldManager(self)

        self.item_manager = ItemManager()

        self.inventory = InventoryHandler()
        self.inventory.initialize_itemstacks(self.item_manager.items, self.save_game_manager.storage['inventory'])

        self.inventory_manager = InventoryManager(self, 'inv_container.png', 'slot.png')
        self.inventory_manager.init_itemstacks(self.inventory.items)

        shop_items = [
            ShopItem(self.item_manager.get_item_by_id(13), 25, "buy"),
            ShopItem(self.item_manager.get_item_by_id(14), 25, "buy"),
            ShopItem(self.item_manager.get_item_by_id(2), 25, "sell")
        ]
        self.shop_manager = ShopManager(self, 'inv_container.png', 'slot.png')
        self.shop_manager.init_itemstacks(shop_items)

        self.overlay_manager = OverlayManager(self)
        self.actions = Settings.player_actions
        self.seed_actions = Settings.player_seed_actions
        self.current_action = 0
        self.current_seed_action = 0

        self.map_manager = Map(self)

        self.pause_state = False
        self.inventory_state = False
        self.shop_state = False
        self.overlay_state = True
        self.running = True

        self.save_game_manager.save_storage(self)

    @property
    def action(self):
        return self.actions[self.current_action]

    @property
    def current_seed(self):
        return self.seed_actions[self.current_seed_action]

    def create_npc(self, pos):
        new_character = WalkingNPC(game=self, options={
            'base': "base",
            'haircut': random.choice(Settings.npc_hair_types),
            'tools': "tools"
        }, size=Settings.npc_size, pos=pos)
        self.characters.add(new_character)

    def run(self):
        while self.running:
            self.clock.tick(Settings.fps)
            self.draw()
            self.update()
            self.watch_for_events()

    def update(self):
        self.cursor.update()
        if self.pause_state:
            pass

        else:
            self.field_manager.update()
            self.characters.update()

            for modal in self.modals:
                modal.update()

    def draw(self):
        self.background.draw(self.screen)
        self.collision_layer.draw(self.screen)
        self.field_manager.draw_fields(self.screen)
        self.characters.draw(self.screen)
        if self.inventory_state:
            self.inventory_manager.draw(self.screen)
        elif self.shop_state:
            self.shop_manager.draw(self.screen)
        else:
            if self.overlay_state:
                self.overlay_manager.draw(self.screen)
            for modal in self.modals:
                modal.draw(self.screen)
        self.cursor.draw(self.screen)
        pygame.display.flip()

    def update_zoom(self):
        self.background.update_zoom(self.background.original_image)
        self.collision_layer.update_zoom(self.collision_layer.original_image)
        self.field_manager.update_zoom()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.save_game_manager.save_storage(self)
                    self.running = False

                if event.key == pygame.K_e:
                    if not self.shop_state:
                        self.inventory_state = not self.inventory_state

                if event.key == pygame.K_p:
                    self.pause_state = not self.pause_state

                if event.key == pygame.K_s:
                    if not self.inventory_state:
                        self.shop_state = not self.shop_state

                if event.key == pygame.K_h:
                    if not self.inventory_state or not self.shop_state:
                        self.overlay_state = not self.overlay_state

                if event.key == pygame.K_UP:
                    if self.current_action != len(self.actions) - 1:
                        self.current_action += 1
                        self.overlay_manager.current_action_item.update_sprite(self.action['icon'])

                if event.key == pygame.K_DOWN:
                    if self.current_action != 0:
                        self.current_action -= 1
                        self.overlay_manager.current_action_item.update_sprite(self.action['icon'])

                if event.key == pygame.K_LEFT:
                    if self.action['name'] == "seed":
                        if self.current_seed_action != 0:
                            self.current_seed_action -= 1
                            self.overlay_manager.current_action_item.update_sprite(self.inventory.find_item(self.current_seed['item_id']).item.image, self.current_seed['path'])

                if event.key == pygame.K_RIGHT:
                    if self.action['name'] == "seed":
                        if self.current_seed_action != len(self.seed_actions) - 1:
                            self.current_seed_action += 1
                            self.overlay_manager.current_action_item.update_sprite(self.inventory.find_item(self.current_seed['item_id']).item.image, self.current_seed['path'])

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.shop_state:
                    self.shop_manager.check_cursor()

            # if event.type == pygame.MOUSEWHEEL:
            # Zoom in
            #     if event.y == 1:
            #         new_zoom = round(self.zoom + Settings.zoom_step, 1)

            # Zoom Out
            #     else:
            #         new_zoom = round(self.zoom - Settings.zoom_step, 1)

            #     if Settings.zoom_max >= new_zoom >= Settings.zoom_min:
            #         self.zoom = new_zoom
            #         self.update_zoom()

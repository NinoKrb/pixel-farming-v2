import random
from classes.cursor import Cursor
from classes.fields import FieldManager
from classes.item import ItemManager
from classes.inventory import InventoryHandler, InventoryManager
from classes.shop import ShopManager, ShopItem
from classes.overlay import OverlayManager
from classes.player import WalkingNPC
from classes.map import Map
from classes.storage import Storage
from classes.music import MusicPlayer
from classes.overlaymenu import *
from classes.alert import AlertManager


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

    def check_collision(self):
        if self.check_cursor_position(self.rect):
            if self.game.cursor.get_pressed((1, 0, 0)):
                self.game.shop_state = True

    def check_cursor_position(self, surface):
        if pygame.Rect.collidepoint(surface, *self.game.cursor.pos):
            return True
        return False


class ShopCollisionLayer(CollisionLayer):
    def __init__(self, game, filename, size, pos):
        self.pos = pos
        self.size = size
        super().__init__(game, filename)

        self.update_zoom(self.image)
        self.set_pos(*self.pos)

    def update_zoom(self, image):
        self.image = pygame.transform.scale(image, (
            int(self.size[0] * self.game.zoom),
            int(self.size[1] * self.game.zoom)
        ))
        self.rect = self.image.get_rect()

    def set_pos(self, x, y):
        self.rect.top = y
        self.rect.left = x


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
        self.inventory_font_small = pygame.font.Font(os.path.join(Settings.path_font, "8-BIT WONDER.TTF"), 10)
        self.inventory_font = pygame.font.Font(os.path.join(Settings.path_font, "8-BIT WONDER.TTF"), 14)
        self.inventory_font_big = pygame.font.Font(os.path.join(Settings.path_font, "8-BIT WONDER.TTF"), 20)

        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()

        self.alert_manager = AlertManager(self)
        self.alert_manager.create_alert("Willkommen bei PixelFarming V2")

        self.music_player = MusicPlayer()

        self.background = ImageLayer(self, "floor.png")
        self.collision_layer = ShopCollisionLayer(self, "collision.png", (80, 64), (368, 32))

        self.cursor = Cursor(Settings.cursors['default'])

        self.field_manager = FieldManager(self)

        self.item_manager = ItemManager()

        self.inventory = InventoryHandler()
        self.inventory.initialize_itemstacks(self.item_manager.items, self.save_game_manager.storage['inventory'])

        self.inventory_manager = InventoryManager(self, 'inv_container.png', 'slot.png')
        self.inventory_manager.init_itemstacks(self.inventory.items)

        shop_items = [ShopItem(self.item_manager.get_item_by_id(item['item_id']), item['price'], item['action']) for item in Settings.shop_items]
        self.shop_manager = ShopManager(self, 'inv_container.png', 'slot.png')
        self.shop_manager.init_itemstacks(shop_items)

        self.overlay_manager = OverlayManager(self)
        self.actions = Settings.player_actions
        self.seed_actions = Settings.player_seed_actions
        self.current_action = 0
        self.current_seed_action = 0

        # Screen Menus
        self.pause_menu = PauseMenu(self)

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

    def quit(self):
        self.save_game_manager.save_storage(self)
        self.running = False

    def run(self):
        while self.running:
            self.clock.tick(Settings.fps)
            self.draw()
            self.update()
            self.watch_for_events()

    def update(self):
        self.cursor.update()
        if not self.pause_state:
            self.field_manager.update()
            self.characters.update()
            self.alert_manager.update()

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
            for modal in self.modals:
                modal.draw(self.screen)

        if self.overlay_state:
            self.overlay_manager.draw(self.screen)

        if self.pause_state:
            self.pause_menu.run()
        else:
            self.alert_manager.draw(self.screen)

        self.cursor.draw(self.screen)
        pygame.display.flip()

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if self.music_player.is_queued():
                    self.music_player.queue_soundtrack()

                else:
                    self.music_player.reset_playlist(True)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.shop_state:
                        self.shop_state = False

                    elif self.inventory_state:
                        self.inventory_state = False

                    else:
                        self.pause_state = not self.pause_state

                if event.key == pygame.K_i:
                    if not self.shop_state:
                        self.inventory_state = not self.inventory_state

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
                            self.overlay_manager.reset_alpha("seed_label")
                            self.overlay_manager.current_action_item.update_sprite(self.inventory.find_item(self.current_seed['item_id']).item.image, self.current_seed['path'])

                if event.key == pygame.K_RIGHT:
                    if self.action['name'] == "seed":
                        if self.current_seed_action != len(self.seed_actions) - 1:
                            self.current_seed_action += 1
                            self.overlay_manager.reset_alpha("seed_label")
                            self.overlay_manager.current_action_item.update_sprite(self.inventory.find_item(self.current_seed['item_id']).item.image, self.current_seed['path'])

            if event.type == pygame.QUIT:
                self.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.shop_state:
                    self.shop_manager.check_cursor()

                else:
                    self.collision_layer.check_collision()


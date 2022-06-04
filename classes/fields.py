import pygame, os, json, csv, random
from settings import Settings
from classes.timer import Timer
from classes.modal import BuyFieldModal


class Field():
    def __init__(self, name, npc_pos, sign_tile, soil_tiles, crop_tiles):
        self.name = name
        self.npc_pos = npc_pos
        self.sign_tile = sign_tile
        self.soil_tiles = soil_tiles
        self.crop_tiles = crop_tiles


class FieldTile(pygame.sprite.Sprite):
    def __init__(self, game, filename, pos, size, path=Settings.path_image):
        super().__init__()
        self.original_image = None
        self.game = game
        self.filename = filename
        self.pos = pos
        self.size = size
        self.path = path
        self.update_sprite(self.filename)

    def update_zoom(self, image):
        self.image = pygame.transform.scale(image, (int(self.size[0] * self.game.zoom), int(self.size[1] * self.game.zoom)))
        self.rect = self.image.get_rect()
        self.set_pos(*self.pos)

    def update_sprite(self, filename):
        self.image = pygame.image.load(os.path.join(self.path, filename)).convert_alpha()
        self.original_image = self.image.copy()
        self.update_zoom(self.image)

    def set_pos(self, x, y):
        self.rect.left = x * self.game.zoom
        self.rect.top = y * self.game.zoom
        self.pos = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class FieldSignTile(FieldTile):
    def __init__(self, game, field, filename, pos, size, path=Settings.path_image):
        super().__init__(game, filename, pos, size, path)
        self.field = field

    def update(self):
        if self.field not in self.game.owned_fields:
            if self.check_cursor_position(self.rect):
                if self.game.cursor.get_pressed((1, 0, 0)):
                    for modal in self.game.modals:
                        try:
                            if modal.field == self.field:
                                modal.visible = True
                        except:
                            pass

    def check_cursor_position(self, surface):
        if pygame.Rect.collidepoint(surface, *self.game.cursor.pos):
            return True
        return False


class CropTile(FieldTile):
    def __init__(self, game, field, attributes, pos, size, growth_state=0):
        super().__init__(game, attributes['fallback_image'], pos, size, Settings.path_crops)
        self.crop_type = attributes
        self.field = field

        self.watering_timer = Timer(self.crop_type['watering_timer'] * random.uniform(*Settings.crop_watering_range))
        self.growth_timer = Timer(self.crop_type['growth_timer'] * random.uniform(*Settings.crop_growth_range))
        self.growth_state = growth_state

        self.is_hovered = False
        self.is_pressed = False
        self.is_watered = False

    def get_growth_state(self, id):
        for tile in self.crop_type['tiles']:
            if tile['growth_state'] == id:
                return tile
        return False

    def update(self):
        self.cursor_logic()
        if self.growth_timer.is_next_stop_reached():
            self.grow()

        if self.watering_timer.is_next_stop_reached():
            self.is_watered = False

        if self.growth_state < -1:
            self.growth_state = -1

    def cursor_logic(self):
        cursor = None
        if self.check_cursor_position():
            if self.growth_state == -1 and self.game.action['name'] == "seed":
                cursor = self.crop_type['seed_cursor']
            elif self.growth_state != self.crop_type['max_growth_state'] and self.game.action['name'] == "water":
                cursor = self.crop_type['hover_cursor']
            else:
                if self.game.action['name'] == "farm":
                    cursor = self.crop_type['max_hover_cursor']

            if cursor:
                if Settings.cursors[cursor] != self.game.cursor.filename:
                    old_pos = self.game.cursor.pos
                    self.game.cursor.update_sprite(Settings.cursors[cursor])
                    self.game.cursor.set_pos(*old_pos)
                    self.is_hovered = True

            if self.game.cursor.get_pressed((1, 0, 0)) and not self.is_pressed:
                if self.growth_state == -1:
                    if self.game.action['name'] == "seed":
                        self.seed()

                elif self.growth_state != self.crop_type['max_growth_state']:
                    if self.game.action['name'] == "water":
                        if not self.is_watered:
                            self.is_watered = True
                            self.grow()

                else:
                    if self.game.action['name'] == "farm":
                        self.harvest()
                self.is_pressed = True
        else:
            if self.is_hovered:
                self.game.cursor.update_sprite(Settings.cursors['default'])
                self.is_hovered = False
                self.is_pressed = False

    def check_cursor_position(self):
        if pygame.Rect.collidepoint(self.rect, *self.game.cursor.pos):
            return True

    def grow(self):
        if self.field in self.game.owned_fields:
            if self.growth_state != -1:
                if self.growth_state != self.crop_type['max_growth_state']:
                    self.growth_state += 1
                    state = self.get_growth_state(self.growth_state)
                    if state:
                        self.update_sprite(state['image'])

    def harvest(self):
        if self.field in self.game.owned_fields:
            state = self.get_growth_state(0)
            self.update_sprite(state['image'])
            self.growth_state = -1

            if self.crop_type['item_id'] != 0:
                self.game.inventory.add_item(self.crop_type['item_id'], 1)
            if self.crop_type['seed_item_id'] != 0:
                self.game.inventory.add_item(self.crop_type['seed_item_id'], 1)
            # self.game.inventory.report()

    def seed(self):
        if self.field in self.game.owned_fields:
            # Update crop type with seed attributes
            if self.crop_type['seed_item_id'] != self.game.current_seed['item_id']:
                self.crop_type = self.game.field_manager.find_crop_type_by_seed(self.game.current_seed['item_id'])

            if self.game.inventory.remove_item(self.crop_type['seed_item_id'], 1):
                state = self.get_growth_state(1)
                self.update_sprite(state['image'])
                self.growth_state = 0

            else:
                print("Not enough Crops")


class FieldManager():
    def __init__(self, game):
        self.game = game
        self.crop_types = self.load_crop_types()
        self.fields = self.load_fields()

    def get_save_able_field_crops(self):
        save_able_crops = []
        for field in self.fields:
            if field.name in self.game.owned_fields:
                for crop_tile in field.crop_tiles:
                    if crop_tile.crop_type['id'] != 0:
                        # Validate Growstate
                        grow_state = crop_tile.growth_state - 1
                        if grow_state < -1:
                            grow_state = -1

                        save_able_crops.append({
                            "crop_id": crop_tile.crop_type['id'],
                            "growth_state": grow_state,
                            "position": {
                                "x": crop_tile.pos[0],
                                "y": crop_tile.pos[1]
                            }
                        })

        return save_able_crops

    def buy_field(self, target_field):
        print(f"Buy target field: {target_field}")
        selected_field = None
        for field in self.fields:
            if field.name == target_field:
                selected_field = field

        if selected_field is not None:
            for tile in selected_field.crop_tiles:
                tile.crop_type = self.crop_types["0"]

            self.game.create_npc(selected_field.npc_pos)
            selected_field.sign_tile.update_sprite("sign_buyed.png")

    def update(self):
        for field in self.fields:
            field.crop_tiles.update()
            field.sign_tile.update()

    def draw_fields(self, screen):
        for field in self.fields:
            field.soil_tiles.draw(screen)
            field.crop_tiles.draw(screen)
            field.sign_tile.draw(screen)

    def load_crop_types(self):
        crop_types = {}

        file = open(os.path.join(Settings.path_storage, Settings.crop_type_filename))
        data = json.load(file)
        file.close()

        for crop in data["crops"]:
            crop_types[f"{crop['id']}"] = crop

        return crop_types

    def find_crop_type_by_seed(self, id):
        for crop_type in self.crop_types.values():
            if crop_type['seed_item_id'] == id:
                return crop_type

    def find_crop_type_by_item(self, id):
        for crop_type in self.crop_types.values():
            if crop_type['item_id'] == id:
                return crop_type

    def update_zoom(self):
        for field in self.fields:
            for tile in field.crop_tiles:
                tile.update_zoom(tile.original_image)

            for tile in field.soil_tiles:
                tile.update_zoom(tile.original_image)

    def find_crop_from_storage(self, x, y):
        for crop in self.game.save_game_manager.storage['crops']:
            if crop['position']['x'] == x:
                if crop['position']['y'] == y:
                    return crop
        return False

    def load_fields(self):
        fields = []
        field_files = os.listdir(Settings.path_fields)
        for field in field_files:
            self.game.modals.append(BuyFieldModal(self.game, field))

            x = 0
            y = 0
            field_tiles = pygame.sprite.Group()
            field_soil_tiles = pygame.sprite.Group()
            sign_tile = None

            with open(os.path.join(Settings.path_fields, field)) as file:
                data = csv.reader(file, delimiter=",")

                for row in data:
                    for col in row:
                        if col != "-1":
                            if col == "2":
                                if field in self.game.owned_fields:
                                    filename = "sign_buyed.png"
                                else:
                                    filename = "sign.png"
                                sign_tile = FieldSignTile(
                                                self.game,
                                                field,
                                                filename,
                                                (x * Settings.tile_width, y * Settings.tile_height),
                                                (Settings.tile_width, Settings.tile_height)
                                            )
                            else:
                                if col == "1":
                                    npc_pos = (x * Settings.tile_width, y * Settings.tile_height)
                                    if field in self.game.owned_fields:
                                        self.game.create_npc((x * Settings.tile_width, y * Settings.tile_height))

                                field_tiles.add(
                                    FieldTile(
                                        self.game,
                                        "farm_soil.png",
                                        (x * Settings.tile_width, y * Settings.tile_height),
                                        (Settings.tile_width, Settings.tile_height)
                                    )
                                )
                                if field in self.game.owned_fields:
                                    # Check if Cropfield is already saved
                                    saved_crop = self.find_crop_from_storage(x * Settings.tile_width, y * Settings.tile_height)
                                    if saved_crop:
                                        # Build Crop Tile from savings
                                        field_soil_tiles.add(
                                            CropTile(
                                                self.game,
                                                field,
                                                self.crop_types[str(saved_crop['crop_id'])],
                                                (saved_crop['position']['x'], saved_crop['position']['y']),
                                                (Settings.tile_width, Settings.tile_height),
                                                saved_crop['growth_state']
                                            )
                                        )

                                    else:
                                        # Generate new Crop Tile
                                        field_soil_tiles.add(
                                            CropTile(
                                                self.game,
                                                field,
                                                self.crop_types["0"],
                                                (x * Settings.tile_width, y * Settings.tile_height),
                                                (Settings.tile_width, Settings.tile_height)
                                            )
                                        )
                                else:
                                    field_soil_tiles.add(
                                        CropTile(
                                            self.game,
                                            field,
                                            self.crop_types["0"],
                                            (x * Settings.tile_width, y * Settings.tile_height),
                                            (Settings.tile_width, Settings.tile_height)
                                        )
                                    )
                        x += 1
                    y += 1
                    x = 0

            fields.append(Field(field, npc_pos, sign_tile, field_tiles, field_soil_tiles))
        return fields

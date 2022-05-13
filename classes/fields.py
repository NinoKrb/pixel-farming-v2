import pygame, os, json, csv, random
from settings import Settings
from classes.timer import Timer

class Field():
    def __init__(self, name, soil_tiles, crop_tiles):
        self.name = name
        self.soil_tiles = soil_tiles
        self.crop_tiles = crop_tiles

class FieldTile(pygame.sprite.Sprite):
    def __init__(self, game, filename, pos, size):
        super().__init__()
        self.game = game
        self.filename = filename
        self.pos = pos
        self.size = size
        self.update_sprite(self.filename, self.pos, self.size)

    def update_sprite(self, filename, pos, size):
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.set_pos(*pos)

    def set_pos(self, x, y):
        self.rect.left = x
        self.rect.top = y
        self.pos = (x,y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class CropTile(FieldTile):
    def __init__(self, game, attributes, pos, size):
        super().__init__(game, attributes['fallback_image'], pos, size)
        self.attributes = attributes

        self.watering_timer = Timer(attributes['watering_timer'] * random.uniform(*Settings.crop_watering_range),)
        self.growth_timer = Timer(attributes['growth_timer'] * random.uniform(*Settings.crop_growth_range),)
        self.growth_state = 0

        self.is_hovered = False
        self.is_pressed = False
        self.is_watered = False

    def get_growth_state(self, id):
        return self.attributes['tiles'][id - 1]

    def update(self):
        self.cursor_logic()
        if self.growth_timer.is_next_stop_reached():
            self.grow()
        if self.watering_timer.is_next_stop_reached():
            self.is_watered = False
            print("RESET WATER TIMER")

    def cursor_logic(self):
        if self.check_cursor_position():
            if self.growth_state != self.attributes['max_growth_state']:
                cursor = self.attributes['hover_cursor']
            else:
                cursor = self.attributes['max_hover_cursor']

            self.game.cursor.update_sprite(Settings.cursors[cursor])
            self.is_hovered = True

            if self.game.cursor.get_pressed((1,0,0)) and self.is_pressed == False:
                if self.growth_state != self.attributes['max_growth_state']:
                    if self.is_watered == False:
                        self.is_watered = True
                        self.grow()
                else:
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
        if self.growth_state != self.attributes['max_growth_state']:
            self.growth_state += 1
            state = self.get_growth_state(self.growth_state)
            self.update_sprite(state['image'], self.pos, self.size)

    def harvest(self):
        state = self.get_growth_state(1)
        print(state)
        self.update_sprite(state['image'], self.pos, self.size)
        print("Harvesting")

    def update_sprite(self, filename, pos, size):
        self.image = pygame.image.load(os.path.join(Settings.path_crops, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.set_pos(*pos)

class FieldManager():
    def __init__(self, game):
        self.game = game
        self.crop_types = self.load_crop_types()
        self.fields = self.load_fields()

    def update(self):
        for field in self.fields:
            field.crop_tiles.update()

    def draw_fields(self,screen):
        for field in self.fields:
            field.soil_tiles.draw(screen)
            field.crop_tiles.draw(screen)

    def load_crop_types(self):
        crop_types = {}

        file = open(os.path.join(Settings.path_storage, Settings.crop_type_filename))
        data = json.load(file)
        file.close()

        for crop in data["crops"]:
            crop_types[f"{crop['id']}"] = crop

        return crop_types

    def load_fields(self):
        fields = []
        field_files = os.listdir(Settings.path_fields)
        for field in field_files:
            x = 0
            y = 0
            field_tiles = pygame.sprite.Group()
            field_soil_tiles = pygame.sprite.Group()

            with open(os.path.join(Settings.path_fields, field)) as file:
                data = csv.reader(file, delimiter=",")

                for row in data:
                    for col in row:
                        if col != "-1":
                            field_tiles.add(FieldTile(self.game, "farm_soil.png", (x * Settings.tile_width, y * Settings.tile_height), (Settings.tile_width, Settings.tile_height)))
                            field_soil_tiles.add(CropTile(self.game, self.crop_types['1'], (x * Settings.tile_width, y * Settings.tile_height), (Settings.tile_width, Settings.tile_height)))
                        x += 1

                    y += 1
                    x = 0

            fields.append(Field(field, field_tiles, field_soil_tiles))
        return fields
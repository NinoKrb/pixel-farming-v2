import os, pygame, csv
from settings import Settings


class BorderTile(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        super().__init__()
        self.size = size
        self.pos = pos
        self.image = pygame.surface.Surface(self.size)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.image.fill((100, 100, 100))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Map():
    def __init__(self, game):
        self.game = game
        self.border_tiles = self.load_layer(self.load_csv(Settings.path_storage, 'map_collision.csv'))

    def load_csv(self, path, filename):
        layer = []
        try:
            with open(os.path.join(path, filename)) as data:
                data = csv.reader(data, delimiter=',')
                for row in data:
                    layer.append(list(row))
            return layer
        except:
            print("CSV File cannot loaded")
            return False

    def load_layer(self, layer):
        layer_sprites = pygame.sprite.Group()
        if layer:
            x, y = 0, 0
            for row in layer:
                for col in row:
                    if col != '-1':
                        if col == "0":
                            layer_sprites.add(BorderTile(Settings.map_tile_size, (x * Settings.map_tile_size[0], y * Settings.map_tile_size[1])))
                    x += 1
                y += 1
                x = 0
        return layer_sprites

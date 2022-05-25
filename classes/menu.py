import pygame, os
from settings import Settings


class MenuSprite(pygame.sprite.Sprite):
    def __init__(self, filename, pos, size, path):
        super().__init__()
        self.filename = filename
        self.pos = pos
        self.size = size
        self.path = path
        self.update_sprite(self.filename, self.pos, self.size)

    def update_sprite(self, filename, pos, size):
        self.image = pygame.image.load(os.path.join(self.path, filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.set_pos(*pos)

    def set_pos(self, x, y):
        self.rect.left = x
        self.rect.top = y
        self.pos = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class MenuSlot():
    def __init__(self, game, slot_img, pos, itemstack=None):
        self.item_label = None
        self.item_sprite = None
        self.slot_sprite = None
        self.slot_img = slot_img
        self.game = game
        self.pos = pos
        self.item_size = Settings.inventory_item_size
        self.slot_size = Settings.inventory_slot_size
        self.itemstack = itemstack
        self.update_sprites()

    def update_itemstack(self, itemstack):
        self.itemstack = itemstack
        self.update_sprites()

    def update_sprites(self):
        self.slot_sprite = MenuSprite(self.slot_img, self.pos, self.slot_size, Settings.path_image)
        if self.itemstack is not None:
            self.item_sprite = MenuSprite(self.itemstack.item.image, (
                self.pos[0] + Settings.inventory_item_slot_offset[0] // 2,
                self.pos[1] + Settings.inventory_item_slot_offset[1] // 2), self.item_size, Settings.path_crops
            )

    def draw(self, screen):
        self.slot_sprite.draw(screen)
        if self.itemstack is not None:
            self.item_label = self.game.inventory_font.render(f"{self.itemstack.amount}", True, (255, 255, 255))
            self.item_sprite.draw(screen)
            screen.blit(self.item_label, (self.pos[0] + self.slot_size[0] - self.item_label.get_width() - 3, self.pos[1] + self.slot_size[1] - self.item_label.get_height() - 5))


class MenuManager():
    def __init__(self, game, background_img, slot_img):
        self.game = game

        pos = (Settings.window_width // 2 - Settings.inventory_size[0] // 2,
               Settings.window_height // 2 - Settings.inventory_size[1] // 2 + 15)
        self.background = MenuSprite(background_img, pos, (450, 450), Settings.path_image)

        self.slots = self.init_grid(pos, Settings.inventory_columns, Settings.inventory_rows, Settings.inventory_offset, slot_img)

    def init_grid(self, start_pos, cols, rows, offset, slot_img):
        slots = []
        max_offset = (cols * offset // 2 - offset, rows * offset // 2 - offset)
        index, x, y = 0, 0, 0
        for row in range(rows):
            for col in range(cols):
                pos = (x * Settings.inventory_slot_size[0] + offset * x + start_pos[0] + max_offset[0],
                       y * Settings.inventory_slot_size[1] + offset * y + start_pos[1] + max_offset[1])
                slots.append(MenuSlot(self.game, slot_img, pos))

                x += 1
                index += 1
            y += 1
            x = 0
        return slots

    def init_itemstacks(self, itemstacks):
        index = 0
        for itemstack in itemstacks:
            self.slots[index].update_itemstack(itemstack)
            index += 1

    def draw(self, screen):
        self.background.draw(screen)
        for slot in self.slots:
            slot.draw(screen)

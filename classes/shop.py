from classes.menu import MenuManager, MenuSlot
from settings import Settings
import pygame


class ShopItem():
    def __init__(self, item, price, action):
        self.item = item
        self.price = price
        self.action = action


class ShopSlot(MenuSlot):
    def __init__(self, game, pos, itemstack=None, price=1):
        super().__init__(game, pos, itemstack)
        self.price = price

    def check_cursor_interaction(self):
        if self.check_cursor_position():
            if self.game.cursor.get_pressed((1, 0, 0)):
                if self.itemstack.action == "buy":
                    if self.game.money >= self.itemstack.price:
                        self.game.money -= self.itemstack.price
                        self.game.inventory.add_item(self.itemstack.item.id, 1)
                        self.game.alert_manager.create_alert("Item gekauft")
                    else:
                        self.game.alert_manager.create_alert("Nicht genug Geld")

                elif self.itemstack.action == "sell":
                    if self.game.inventory.get_amount_by_id(self.itemstack.item.id) >= 1:
                        self.game.money += self.itemstack.price
                        self.game.inventory.remove_item(self.itemstack.item.id, 1)
                        self.game.alert_manager.create_alert("Item verkauft")
                    else:
                        self.game.alert_manager.create_alert("Nicht genug Items")

    def check_cursor_position(self):
        if self.item_sprite:
            if pygame.Rect.collidepoint(self.item_sprite.rect, *self.game.cursor.pos):
                return True
        return False

    def draw(self, screen):
        self.slot_sprite.draw(screen)
        if self.itemstack is not None:
            if self.itemstack.action == "buy":
                color = (194, 0, 0)
            elif self.itemstack.action == "sell":
                color = (0, 194, 13)
            else:
                color = (255, 255, 255)
            self.item_label = self.game.inventory_font.render(f"{self.itemstack.price}", True, color)
            self.item_sprite.draw(screen)
            screen.blit(self.item_label, (self.pos[0] + self.slot_size[0] - self.item_label.get_width() - 3, self.pos[1] + self.slot_size[1] - self.item_label.get_height() - 5))


class ShopManager(MenuManager):
    def __init__(self, game, background_img, slot_img):
        super().__init__(game, background_img, slot_img)

    def init_grid(self, start_pos, cols, rows, offset, slot_img):
        slots = []
        max_offset = (cols * offset // 2 - offset, rows * offset // 2 - offset)
        index, x, y = 0, 0, 0
        for row in range(rows):
            for col in range(cols):
                pos = (x * Settings.inventory_slot_size[0] + offset * x + start_pos[0] + max_offset[0],
                       y * Settings.inventory_slot_size[1] + offset * y + start_pos[1] + max_offset[1])
                slots.append(ShopSlot(self.game, slot_img, pos))

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

    def check_cursor(self):
        for slot in self.slots:
            slot.check_cursor_interaction()

    def draw(self, screen):
        self.background.draw(screen)
        for slot in self.slots:
            slot.draw(screen)

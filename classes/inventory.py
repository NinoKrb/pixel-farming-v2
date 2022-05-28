import pygame, os
from settings import Settings
from classes.menu import MenuManager, MenuSlot


class ItemStack():
    def __init__(self, item, amount):
        self.item = item
        self.amount = amount


class InventoryHandler():
    def __init__(self):
        self.items = []

    def initialize_itemstacks(self, items, saved_items):
        for item in items:
            item_amount = 0
            for saved_item in saved_items:
                if saved_item['item_id'] == item.id:
                    item_amount = saved_item['amount']
            self.items.append(ItemStack(item, item_amount))

    def report(self):
        for item in self.items:
            print(item.item.name, item.amount)

    def add_item(self, id, amount):
        itemstack = self.find_item(id)
        itemstack.amount += amount

    def remove_item(self, id, amount):
        itemstack = self.find_item(id)
        if itemstack.amount >= amount:
            itemstack.amount -= amount
            return itemstack.amount
        else:
            return False

    def get_amount_by_id(self, id):
        itemstack = self.find_item(id)
        return itemstack.amount

    def find_item(self, id):
        for item in self.items:
            if item.item.id == id:
                return item

    def get_storage_inventory(self):
        inventory_storage = []
        for item in self.items:
            inventory_storage.append({
                "item_id": item.item.id,
                "amount": item.amount
            })
        return inventory_storage


class InventorySlot(MenuSlot):
    def __init__(self, game, pos, itemstack=None):
        super().__init__(game, pos, itemstack)


class InventoryManager(MenuManager):
    def __init__(self, game, background_img, slot_img):
        super().__init__(game, background_img, slot_img)

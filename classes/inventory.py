class ItemStack():
    def __init__(self, item, amount):
        self.item = item
        self.amount = amount

class Inventory():
    def __init__(self):
        self.items = []

    def initialize_itemstacks(self, items):
        for item in items:
            self.items.append(ItemStack(item, 0))

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

    def find_item(self, id):
        for item in self.items:
            if item.item.id == id:
                return item

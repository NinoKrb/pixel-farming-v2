import os, json
from settings import Settings


class Item():
    def __init__(self, id, name, filename):
        self.id = id
        self.name = name
        self.image = filename


class ItemManager():
    def __init__(self):
        self.items = self.load_items()

    def load_items(self):
        items = []

        file = open(os.path.join(Settings.path_storage, Settings.item_type_filename))
        data = json.load(file)
        file.close()

        for item in data["items"]:
            items.append(Item(item['id'], item['name'], item['image']))

        return items

    def get_item_by_id(self, id):
        for item in self.items:
            if item.id == id:
                return item

    def get_item_by_name(self, name):
        for item in self.items:
            if item.name == name:
                return item

from settings import Settings
import os, json


class Storage():
    def __init__(self, game):
        self.game = game
        self.save_game = "1"  # ID from the Save Game
        self.filename = Settings.storage_filename
        self.path = Settings.path_storage

        self.storage = self.load_storage()
        if not self.storage:
            self.create_save_game(self.save_game)
            self.save_storage(self.game)
            self.storage = self.load_storage()

    def create_save_game(self, save_game_id):
        data, file = self.load_save_games()
        new_save_game = {
            "id": save_game_id,
            "money": "",
            "owned_fields": [],
            "inventory": [],
            "crops": []
        }
        data['save_games'].append(new_save_game)
        self.save_save_games(file, data)

    def load_save_games(self):
        file = open(os.path.join(self.path, self.filename), 'r+')
        data = json.load(file)
        return data, file

    def save_save_games(self, file, data):
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

    def load_storage(self):
        data, file = self.load_save_games()
        for scoreset in data['save_games']:
            if scoreset['id'] == self.save_game:
                return scoreset
        return False

    def save_storage(self, game=None):
        if game is None:
            game = self.game
        data, file = self.load_save_games()
        for score_set in data['save_games']:
            if score_set['id'] == self.save_game:
                score_set['money'] = game.money
                score_set['owned_fields'] = game.owned_fields
                score_set['inventory'] = game.inventory.get_storage_inventory()
                score_set['crops'] = game.field_manager.get_save_able_field_crops()

        self.save_save_games(file, data)

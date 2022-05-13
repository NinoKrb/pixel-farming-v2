import os, csv

class Settings(object):
    title = "Pixel Farming V2"

    window_width = 800
    window_height = 800

    tile_width = 16
    tile_height = 16
    
    fps = 60

    path_file = os.path.dirname(os.path.abspath(__file__))
    path_assets = os.path.join(path_file, "assets")
    path_image = os.path.join(path_assets, "images")
    path_crops = os.path.join(path_image, "crops")
    path_cursors = os.path.join(path_image, "cursors")

    path_storage = os.path.join(path_file, "storage")
    path_fields = os.path.join(path_storage, "fields")

    crop_type_filename = "crops.json"
    crop_growth_range = (1.5, 2.5)
    crop_watering_range =  (1, 1)

    player_size = (80,80)
    player_spawn_position = (0,0)

    cursor_size = (24,24)
    cursors = {
        "default": "cursor_01.png",
        "hammer": "hammer.png",
        "pickaxe": "pickaxe.png",
        "shovel": "shovel.png",
        "sword": "sword.png",
        "axe": "axe.png",
        "water": "water.png",
        "hand_1_open": "hand_open_01.png",
        "hand_1_closed": "hand_closed_01.png",
        "hand_2_open": "hand_open_02.png",
        "hand_2_closed": "hand_closed_02.png"
    }

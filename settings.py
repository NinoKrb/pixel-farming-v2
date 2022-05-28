import os


class Settings(object):
    title = "Pixel Farming V2"

    window_width = 800
    window_height = 800

    tile_width = 16
    tile_height = 16

    zoom_default = 1
    zoom_max = 2.5
    zoom_min = 1
    zoom_step = 0.1

    fps = 60

    path_file = os.path.dirname(os.path.abspath(__file__))
    path_assets = os.path.join(path_file, "assets")
    path_image = os.path.join(path_assets, "images")
    path_font = os.path.join(path_assets, "fonts")
    path_crops = os.path.join(path_image, "crops")
    path_cursors = os.path.join(path_image, "cursors")
    path_icons = os.path.join(path_image, "icons")

    path_storage = os.path.join(path_file, "storage")
    path_fields = os.path.join(path_storage, "fields")

    crop_type_filename = "crops.json"
    crop_growth_range = (1.5, 2.5)
    crop_watering_range = (1, 1)

    replant_time = 100000

    cursor_size = (19, 19)
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

    item_type_filename = "items.json"

    inventory_size = (450, 450)
    inventory_slot_size = (45, 45)
    inventory_item_size = (29, 29)
    inventory_item_slot_offset = (14, 14)
    inventory_offset = 12
    inventory_columns = 7
    inventory_rows = 7

    npc_size = (80, 80)
    npc_directions = ["up", "down", "left", "right"]
    npc_offset_range = (-1, 1)
    npc_speed_range = (0, 1)
    npc_hair_types = [
        "longhair",
        "curlyhair",
        "spikeyhair",
        "mophair",
        "shorthair",
        "bowlhair"
    ]

    map_tile_size = (16, 16)

    player_actions = [
            {
                "name": "cursor",
                "icon": "hand_open_02.png",
                "path": path_icons
            },
            {
                "name": "seed",
                "icon": "plant_alt.png",
                "path": path_icons
            },
            {
                "name": "farm",
                "icon": "shovel.png",
                "path": path_icons
            },
            {
                "name": "water",
                "icon": "water.png",
                "path": path_icons
            }
        ]

    storage_filename = "storage.json"

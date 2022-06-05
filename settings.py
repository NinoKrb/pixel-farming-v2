import os


class Settings(object):
    title = "Pixel Farming V2"

    window_width = 800
    window_height = 800

    tile_width = 16
    tile_height = 16

    start_money = 25000

    zoom_default = 1
    zoom_max = 2.5
    zoom_min = 1
    zoom_step = 0.1

    fps = 60

    path_file = os.path.dirname(os.path.abspath(__file__))
    path_assets = os.path.join(path_file, "assets")
    path_image = os.path.join(path_assets, "images")
    path_font = os.path.join(path_assets, "fonts")
    path_sounds = os.path.join(path_assets, "sounds")
    path_crops = os.path.join(path_image, "crops")
    path_cursors = os.path.join(path_image, "cursors")
    path_icons = os.path.join(path_image, "icons")
    path_texts = os.path.join(path_image, "text")
    path_soundtracks = os.path.join(path_sounds, "soundtracks")

    path_storage = os.path.join(path_file, "storage")
    path_fields = os.path.join(path_storage, "fields")

    crop_type_filename = "crops.json"
    crop_growth_range = (1.5, 2.5)
    crop_watering_range = (1, 1)

    field_prices = {
        "map_field_1.csv": 25000,
        "map_field_2.csv": 25000,
        "map_field_3.csv": 50000,
        "map_field_4.csv": 50000,
        "map_field_5.csv": 75000,
        "map_field_6.csv": 100000
    }

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

    player_seed_actions = [
        {
            "title": "Rote Beete",
            "item_id": 12,
            "path": path_crops
        },
        {
            "title": "Kraut",
            "item_id": 13,
            "path": path_crops
        },
        {
            "title": "Blumenkohl",
            "item_id": 14,
            "path": path_crops
        },
        {
            "title": "Grünkohl",
            "item_id": 15,
            "path": path_crops
        },
        {
            "title": "Pastinake",
            "item_id": 16,
            "path": path_crops
        },
        {
            "title": "Kürbis",
            "item_id": 17,
            "path": path_crops
        },
        {
            "title": "Kartoffel",
            "item_id": 18,
            "path": path_crops
        },
        {
            "title": "Radischen",
            "item_id": 19,
            "path": path_crops
        },
        {
            "title": "Sonnenblume",
            "item_id": 20,
            "path": path_crops
        },
        {
            "title": "Karotte",
            "item_id": 21,
            "path": path_crops
        },
        {
            "title": "Weizen",
            "item_id": 22,
            "path": path_crops
        }
    ]

    shop_items = [
        {
            "item_id": 12,
            "price": 25,
            "action": "buy"
        },
        {
            "item_id": 13,
            "price": 25,
            "action": "buy"
        },
        {
            "item_id": 14,
            "price": 25,
            "action": "buy"
        },
        {
            "item_id": 15,
            "price": 25,
            "action": "buy"
        },
        {
            "item_id": 16,
            "price": 25,
            "action": "buy"
        },
        {
            "item_id": 17,
            "price": 25,
            "action": "buy"
        },
        {
            "item_id": 18,
            "price": 25,
            "action": "buy"
        },
        {
            "item_id": 19,
            "price": 25,
            "action": "buy"
        },
        {
            "item_id": 20,
            "price": 25,
            "action": "buy"
        },
        {
            "item_id": 21,
            "price": 25,
            "action": "buy"
        },
        {
            "item_id": 22,
            "price": 25,
            "action": "buy"
        },
        {
            "item_id": 1,
            "price": 75,
            "action": "sell"
        },
        {
            "item_id": 2,
            "price": 75,
            "action": "sell"
        },
        {
            "item_id": 3,
            "price": 75,
            "action": "sell"
        },
        {
            "item_id": 4,
            "price": 75,
            "action": "sell"
        },
        {
            "item_id": 5,
            "price": 75,
            "action": "sell"
        },
        {
            "item_id": 6,
            "price": 75,
            "action": "sell"
        },
        {
            "item_id": 7,
            "price": 75,
            "action": "sell"
        },
        {
            "item_id": 8,
            "price": 75,
            "action": "sell"
        },
        {
            "item_id": 9,
            "price": 75,
            "action": "sell"
        },
        {
            "item_id": 10,
            "price": 75,
            "action": "sell"
        },
        {
            "item_id": 11,
            "price": 75,
            "action": "sell"
        },
        {
            "item_id": 12,
            "price": 75,
            "action": "sell"
        }
    ]

    default_playlist = [
        os.path.join(path_soundtracks, "Soundtrack_1.wav"),
        os.path.join(path_soundtracks, "Soundtrack_2.wav"),
        os.path.join(path_soundtracks, "Soundtrack_3.wav"),
        os.path.join(path_soundtracks, "Soundtrack_4.wav")
    ]

    overlay_alpha_timer = 100
    overlay_alpha_step = 25
    overlay_alpha_max = 255

    alert_pos = (25, 25)
    alert_color = (255, 255, 255)
    alert_duration = 2000

    storage_filename = "storage.json"

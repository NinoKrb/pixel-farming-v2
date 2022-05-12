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

    path_storage = os.path.join(path_file, "storage")
    path_fields = os.path.join(path_storage, "fields")

    crop_type_filename = "crops.json"
    
    crop_growth_range = (0.5, 1.5)

    player_size = (80,80)
    player_spawn_position = (0,0)

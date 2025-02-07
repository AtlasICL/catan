class GameParameters:
    # Width and Height for the game window in pixels
    GAME_WIDTH: int = 700
    GAME_HEIGHT: int = 700

    # Size of hexagons in pixels
    TILE_SIZE: int = 60

    # Board radius, measured as tiles from the center tile
    BOARD_RADIUS: int = 2

    # Resources types on the board
    FIXED_RESOURCES = [
        "Wood", "Sheep", "Ore", "Brick", "Sheep",
        "Brick", "Wheat", "Ore", "Wood", "Desert",
        "Wood", "Wheat", "Sheep", "Wheat", "Ore",
        "Wood", "Sheep", "Wheat", "Brick"
    ]

    # The number values corresponding to the resource types on the board
    # None is the 'Desert' tile, which does not have a number value in the game
    NUMBER_TOKENS = [
        9, 2, 10, 10, 4,
        6, 12, 8, 3, None,
        11, 9, 5, 4, 3,
        8, 11, 6, 5
    ]

    # The ports around the edge of the board
    # Template: (type, x_coordinate, y_coordinate)
    # 3:1 designates a port in which 3 of any resource can be traded for 1 of another
    # "Wood", "Brick" etc denote a port in which 2 of the names resource can be traded for 1 of another
    PORTS = [
        ("3:1", -2, 0),
        ("Wood", -1, 2),
        ("Brick", 1, 2),
        ("3:1", 2, 1),
        ("Wheat", 2, -1),
        ("Sheep", 1, -2),
        ("Ore", -1, -2),
        ("3:1", -2, -1),
        ("3:1", -2, 1),
    ]

    # This one is a mess, and was a dodgy workaround used in the 
    # get_nearest_intersection function in board.py
    NEIGHBOR_DELTAS = [
        (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)
    ]

    # Hex colours corresponding to each resource type
    # For drawing on the board
    RESOURCE_COLORS = {
        "Wood": "#228B22",
        "Brick": "#964B00",
        "Sheep": "#ADFF2F",
        "Wheat": "#FFD700",
        "Ore": "#A9A9A9",
        "Desert": "#D2B48C",
        "Dice": "#FCFBF4"
    }
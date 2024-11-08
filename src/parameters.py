class GameParameters:
    GAME_WIDTH: int = 700
    GAME_HEIGHT: int = 700

    TILE_SIZE: int = 60
    BOARD_RADIUS: int = 2

    FIXED_RESOURCES = [
        "Wood", "Sheep", "Ore", "Brick", "Sheep",
        "Brick", "Wheat", "Ore", "Wood", "Desert",
        "Wood", "Wheat", "Sheep", "Wheat", "Ore",
        "Wood", "Sheep", "Wheat", "Brick"
    ]

    NUMBER_TOKENS = [
        9, 2, 10, 10, 4,
        6, 12, 8, 3, None,
        11, 9, 5, 4, 3,
        8, 11, 6, 5
    ]

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

    RESOURCE_COLORS = {
        "Wood": "#228B22",
        "Brick": "#964B00",
        "Sheep": "#ADFF2F",
        "Wheat": "#FFD700",
        "Ore": "#A9A9A9",
        "Desert": "#D2B48C",
        "Dice": "#FCFBF4"
    }
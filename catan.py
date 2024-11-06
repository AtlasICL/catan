import tkinter as tk
import math
import random

GAME_WIDTH: int = 800
GAME_HEIGHT: int = 800

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

RESOURCE_COLORS = {
    "Wood": "#228B22",
    "Brick": "#B22222",
    "Sheep": "#ADFF2F",
    "Wheat": "#FFD700",
    "Ore": "#A9A9A9",
    "Desert": "#D2B48C"
}

class CatanBoard(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, width=GAME_WIDTH, height=GAME_HEIGHT, bg="lightblue")
        self.pack()
        self.tiles = []
        self.create_board()

    def create_board(self):
        resource_index: int = 0
        number_index: int = 0
        for q in range(-BOARD_RADIUS, BOARD_RADIUS + 1):
            for r in range(-BOARD_RADIUS, BOARD_RADIUS + 1):
                if abs(q + r) <= BOARD_RADIUS:
                    x, y = self.hex_to_pixel(q, r)
                    resource_type = FIXED_RESOURCES[resource_index]
                    number_token = NUMBER_TOKENS[number_index]
                    resource_index += 1
                    number_index += 1
                    self.draw_hexagon(x, y, resource_type, number_token)

    def hex_to_pixel(self, q, r):
        x = TILE_SIZE * (3/2 * q)
        y = TILE_SIZE * (math.sqrt(3) * (r + q / 2))
        center_x = GAME_WIDTH / 2
        center_y = GAME_HEIGHT / 2
        return x + center_x, y + center_y

    def draw_hexagon(self, x, y, resource_type, number_token):
        points = []
        for i in range(6):
            angle = 2 * math.pi / 6 * i
            x_i = x + TILE_SIZE * math.cos(angle)
            y_i = y + TILE_SIZE * math.sin(angle)
            points.extend([x_i, y_i])

        color = RESOURCE_COLORS[resource_type]
        self.create_polygon(points, outline="black", fill=color, width=2)
        self.create_text(x, y-20, text=resource_type, fill="black", font=("Arial", 10))
        if number_token is not None:
            self.create_oval(x - 15, y - 15, x + 15, y + 15, fill="white", outline="black")
            self.create_text(x, y, text=str(number_token), fill="black", font=("Arial", 12, "bold"))


class CatanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Catan Clone")
        self.board = CatanBoard(root)

if __name__ == "__main__":
    root = tk.Tk()
    game = CatanGame(root)
    root.mainloop()

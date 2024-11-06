import tkinter as tk
import math
import random

class GameParameters:
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
        "Brick": "#964B00",
        "Sheep": "#ADFF2F",
        "Wheat": "#FFD700",
        "Ore": "#A9A9A9",
        "Desert": "#D2B48C"
    }



class CatanBoard(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, width=GameParameters.GAME_WIDTH, height=GameParameters.GAME_HEIGHT, bg="lightblue")
        self.pack()
        self.tiles = []
        self.bandit_id = None
        self.bandit_position = None
        self.create_board()


    def create_board(self):
        resource_index: int = 0
        number_index: int = 0
        for q in range(-GameParameters.BOARD_RADIUS, GameParameters.BOARD_RADIUS + 1):
            for r in range(-GameParameters.BOARD_RADIUS, GameParameters.BOARD_RADIUS + 1):
                if abs(q + r) <= GameParameters.BOARD_RADIUS:
                    x, y = self.hex_to_pixel(q, r)
                    resource_type = GameParameters.FIXED_RESOURCES[resource_index]
                    number_token = GameParameters.NUMBER_TOKENS[number_index]
                    resource_index += 1
                    number_index += 1
                    self.draw_hexagon(x, y, resource_type, number_token)
        self.draw_bandit(0, 0)


    def hex_to_pixel(self, q, r):
        x = GameParameters.TILE_SIZE * (3/2 * q)
        y = GameParameters.TILE_SIZE * (math.sqrt(3) * (r + q / 2))
        center_x = GameParameters.GAME_WIDTH / 2
        center_y = GameParameters.GAME_HEIGHT / 2
        return x + center_x, y + center_y
    
    def pixel_to_hex(self, x, y):
        center_x = GameParameters.GAME_WIDTH / 2
        center_y = GameParameters.GAME_HEIGHT / 2

        q = (2/3 * (x - center_x)) / GameParameters.TILE_SIZE
        r = (-1/3 * (x - center_x) + math.sqrt(3)/3 * (y - center_y)) / GameParameters.TILE_SIZE
        return self.round_hex(q, r)
    
    def round_hex(self, q, r):
        q_rounded = round(q)
        r_rounded = round(r)
        s_rounded = round(-q - r)
        
        q_diff = abs(q_rounded - q)
        r_diff = abs(r_rounded - r)
        s_diff = abs(s_rounded + q + r)
        
        if q_diff > r_diff and q_diff > s_diff:
            q_rounded = -r_rounded - s_rounded
        elif r_diff > s_diff:
            r_rounded = -q_rounded - s_rounded
            
        return q_rounded, r_rounded



    def draw_hexagon(self, x, y, resource_type, number_token):
        points = []
        for i in range(6):
            angle = 2 * math.pi / 6 * i
            x_i = x + GameParameters.TILE_SIZE * math.cos(angle)
            y_i = y + GameParameters.TILE_SIZE * math.sin(angle)
            points.extend([x_i, y_i])

        color = GameParameters.RESOURCE_COLORS[resource_type]
        self.create_polygon(points, outline="black", fill=color, width=2)
        self.create_text(x, y-25, text=resource_type, fill="black", font=("Arial", 10, "bold"))
        if number_token is not None:
            self.create_oval(x - 15, y - 15, x + 15, y + 15, fill="white", outline="black")
            self.create_text(x, y, text=str(number_token), fill="black", font=("Arial", 12))


    def draw_bandit(self, q, r):
        if self.bandit_id is not None:
            self.delete(self.bandit_id)
        x, y = self.hex_to_pixel(q, r)
        self.bandit_id = self.create_oval(x+10, y+10, x+35, y+35, fill="black", outline="orange")
        self.bandit_position = (q, r)

    def start_drag(self, event):
        """Initiate dragging if the bandit is clicked."""
        if self.bandit_id is not None:
            # Check if the click is on the bandit
            x, y = self.coords(self.bandit_id)[:2]  # Get bandit's current coordinates
            if abs(event.x - (x + 15)) < 15 and abs(event.y - (y + 15)) < 15:
                self.bind("<B1-Motion>", self.drag_bandit)
                self.bind("<ButtonRelease-1>", self.drop_bandit)

    def drag_bandit(self, event):
        """Drag the bandit along with the mouse."""
        if self.bandit_id is not None:
            self.coords(self.bandit_id, event.x - 15, event.y - 15, event.x + 15, event.y + 15)

    def drop_bandit(self, event):
        """Drop the bandit and snap to the nearest hex center."""
        # Unbind dragging events
        self.unbind("<B1-Motion>")
        self.unbind("<ButtonRelease-1>")
        
        # Snap to the nearest hex
        q, r = self.pixel_to_hex(event.x, event.y)
        self.draw_bandit(q, r)  # Redraw bandit at the nearest hex


class CatanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Catan Clone")
        self.board = CatanBoard(root)      
        self.bandit_button = tk.Button(root, text="Random Bandit", command=self.place_bandit)
        self.bandit_button.pack(pady=10)
        self.board.bind("<Button-1>", self.board.start_drag)

    def place_bandit(self):
        q = random.randint(-GameParameters.BOARD_RADIUS, GameParameters.BOARD_RADIUS)
        max_r = GameParameters.BOARD_RADIUS - abs(q)
        r = random.randint(-max_r, max_r)
        self.board.draw_bandit(q, r)



        
if __name__ == "__main__":
    root = tk.Tk()
    game = CatanGame(root)
    root.mainloop()
    



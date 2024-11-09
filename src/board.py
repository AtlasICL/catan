import math
import tkinter as tk

from village import Village
from parameters import GameParameters
from dice import DiceRoll


class CatanBoard(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, width=GameParameters.GAME_WIDTH, height=GameParameters.GAME_HEIGHT, bg="lightblue")
        self.pack()
        self.tiles = []
        self.bandit_id = None
        self.bandit_position = None
        self.village_circle = None
        self.placing_village = False
        self.villages = []
        self.village_circles = []
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
        self.display_dice(-3, -1, DiceRoll(2, 4))


    def display_dice(self, q, r, dice_roll):
        a, b = self.hex_to_pixel(q, r)
        self.draw_hexagon(a, b, "Dice", None)
        self.create_rectangle(a + 5, b - 0, a + 35, b + 30, fill="white", outline="black")
        self.create_rectangle(a - 35, b - 0, a - 5, b + 30, fill="white", outline="black")
        self.create_text(a + 20, b + 15, text=str(dice_roll.die1), fill="black", font=("Arial", 12, "bold"))
        self.create_text(a - 20, b + 15, text=str(dice_roll.die2), fill="black", font=("Arial", 12, "bold"))

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
        if self.bandit_id is not None:
            # check if the click is on the bandit
            x, y = self.coords(self.bandit_id)[:2]  # get bandits current coordinates
            if abs(event.x - (x + 15)) < 15 and abs(event.y - (y + 15)) < 15:
                self.bind("<B1-Motion>", self.drag_bandit)
                self.bind("<ButtonRelease-1>", self.drop_bandit)

    def drag_bandit(self, event):
        if self.bandit_id is not None:
            self.coords(self.bandit_id, event.x - 15, event.y - 15, event.x + 15, event.y + 15)

    def drop_bandit(self, event):
        self.unbind("<B1-Motion>")
        self.unbind("<ButtonRelease-1>")
        
        q, r = self.pixel_to_hex(event.x, event.y)
        self.draw_bandit(q, r)

    def start_village_placement(self):
        self.placing_village = True
        self.bind("<Motion>", self.move_village_with_cursor)
        self.bind("<Button-1>", self.place_village)

    def move_village_with_cursor(self, event):
        if self.placing_village:
            if self.village_circle is None:
                radius = 10
                self.village_circle = self.create_oval(event.x - radius, event.y - radius, event.x + radius, event.y + radius, fill="blue", outline="black")
            else:
                radius = 10
                self.coords(self.village_circle, event.x - radius, event.y - radius, event.x + radius, event.y + radius)

    def place_village(self, event):
        if self.placing_village:
            nearest_x, nearest_y = self.get_nearest_intersection(event.x, event.y)

            new_village = Village(nearest_x, nearest_y)
            self.villages.append(new_village)

            radius = 10
            village_circle_id = self.create_oval(nearest_x - radius, nearest_y - radius, nearest_x + radius, nearest_y + radius, fill="blue", outline="black")
            self.village_circles.append(village_circle_id)

            if self.village_circle is not None:
                self.delete(self.village_circle)
                self.village_circle = None

            self.unbind("<Motion>")
            self.unbind("<Button-1>")
            self.placing_village = False

    def get_nearest_intersection(self, x, y):
        nearest_point = None
        min_distance = float('inf')
        
        neighbor_deltas = GameParameters.NEIGHBOR_DELTAS
        
        for q in range(-GameParameters.BOARD_RADIUS, GameParameters.BOARD_RADIUS + 1):
            for r in range(-GameParameters.BOARD_RADIUS, GameParameters.BOARD_RADIUS + 1):
                if abs(q + r) <= GameParameters.BOARD_RADIUS:
                    center_x, center_y = self.hex_to_pixel(q, r)
                    for i in range(len(neighbor_deltas)):
                        for j in range(i + 1, len(neighbor_deltas)):
                            dq1, dr1 = neighbor_deltas[i]
                            dq2, dr2 = neighbor_deltas[j]

                            neighbor1_x, neighbor1_y = self.hex_to_pixel(q + dq1, r + dr1)
                            neighbor2_x, neighbor2_y = self.hex_to_pixel(q + dq2, r + dr2)

                            px = (center_x + neighbor1_x + neighbor2_x) / 3
                            py = (center_y + neighbor1_y + neighbor2_y) / 3

                            dist = math.sqrt((x - px) ** 2 + (y - py) ** 2)

                            if dist < min_distance:
                                min_distance = dist
                                nearest_point = (px, py)

        return nearest_point if nearest_point else (x, y)

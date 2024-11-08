import tkinter as tk
import random
from dataclasses import dataclass

from parameters import GameParameters
from board import CatanBoard
from dice import DiceRoll


class CatanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Catan Clone")
        self.board = CatanBoard(root)      
        self.bandit_button = tk.Button(root, text="Random Bandit", command=self.place_bandit)
        self.bandit_button.pack(pady=2)
        self.dice_roll_button = tk.Button(root, text="Roll Dice", command=self.roll_dice)
        self.dice_roll_button.pack(pady=2)
        self.board.bind("<Button-1>", self.board.start_drag)

    def roll_dice(self):
        dice_roll = DiceRoll(random.randint(1, 6), random.randint(1, 6))
        self.board.display_dice(-3, -1, dice_roll)

    def place_bandit(self):
        q = random.randint(-GameParameters.BOARD_RADIUS, GameParameters.BOARD_RADIUS)
        max_r = GameParameters.BOARD_RADIUS - abs(q)
        r = random.randint(-max_r, max_r)
        self.board.draw_bandit(q, r)



        

    



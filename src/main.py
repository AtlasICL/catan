import tkinter as tk
import math
import random
from dataclasses import dataclass

from game import CatanGame

if __name__ == "__main__":
    root = tk.Tk()
    game = CatanGame(root)
    root.mainloop()
import tkinter as tk

from game import CatanGame

if __name__ == "__main__":
    root = tk.Tk()
    game = CatanGame(root)
    root.mainloop()
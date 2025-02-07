from dataclasses import dataclass

@dataclass
class DiceRoll:
    die1: int = 0
    die2: int = 0

    def cout(self) -> None:
        """
        Debugging function to print the values of the dice to the console
        """
        print(f"({self.die1=}, {self.die2=})")


# The functionality for the dice is somewhat weirdly divided 
# between the roll_dice function of CatanGame class
# and the DiceRoll class defined in this file.
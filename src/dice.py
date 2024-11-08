from dataclasses import dataclass

@dataclass
class DiceRoll:
    die1: int = 0
    die2: int = 0

    def cout(self) -> None:
        print(f"({self.die1=}, {self.die2=})")
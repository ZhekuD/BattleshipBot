from BattleshipGame.rules import Ship
from pathlib import Path


class Interface:
    def __init__(self):
        with open(Path(__file__).resolve().parent.joinpath('field_pattern'), 'r') as file:
            field_pattern = file.read()

        self.field_pattern = field_pattern

    def field_render(self, player, field):
        data = []
        for line in getattr(player, field):
            for block in line:

                if isinstance(block, Ship):
                    data.append('o')
                else:
                    data.append(' ')
        gfield = self.field_pattern.format(*data)
        print(gfield)

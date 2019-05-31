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
                    data.append('[38;5;226m{}[0m'.format('■'))
                elif block == 'miss' or block == 8:
                    data.append('[37m{}[0m'.format('◯'))
                elif block == 'hit':
                    data.append('[31;1;5m{}[0m'.format('x'))
                elif block == 1:
                    data.append('[31;1m{}[0m'.format('x'))
                else:
                    data.append(' ')
        gfield = self.field_pattern.format(*data)
        print(gfield)

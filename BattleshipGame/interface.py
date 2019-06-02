from BattleshipGame.rules import Ship
from pathlib import Path


class Interface:
    def __init__(self):
        with open(Path(__file__).resolve().parent.joinpath('field_pattern'), 'r') as file:
            field_pattern = file.read()

        self.field_pattern = field_pattern

    def field_render(self, player, field=''):
        def analyser(f):
            data = []
            for line in getattr(player, f):
                for block in line:
                    if isinstance(block, Ship):
                        data.append('[38;5;226m{}[0m'.format('■'))
                    elif block == 2:
                        data.append(('[31;1;5m{}[0m'.format('□')))
                    elif block == 'miss' or block == 8:
                        data.append('{}'.format('◯'))  # '[37m{}[0m'
                    elif block == 'hit':
                        data.append('[31;1;5m{}[0m'.format('x'))
                    elif block == 1:
                        data.append('[31;1m{}[0m'.format('x'))
                    else:
                        data.append(' ')
            return data

        if not field:
            gfield = ''
            field_data = self.field_pattern.format(*analyser('field'))
            enemy_filed_data = self.field_pattern.format(*analyser('enemy_field'))
            for x, y in zip(field_data.splitlines(), enemy_filed_data.splitlines()):
                gfield += x + '    ' + y + '\n'
        else:
            result = analyser(field)
            gfield = self.field_pattern.format(*result)

        print(gfield)

from BattleshipGame.rules import Player, Ship
from os.path import abspath, curdir


class Interface:
    def __init__(self):
        with open(abspath(curdir) + '/field_pattern', 'r') as file:
            field_pattern = file.read()

        self.field_pattern = field_pattern

    def field_render(self, player, field):
        data = []
        for line in getattr(player, field):
            for block in line:
                # print(type(block), ' = ', Ship)

                if isinstance(block, Ship):
                    data.append('o')
                else:
                    data.append(' ')
        gfield = self.field_pattern.format(*data)
        print(gfield)


if __name__ == "__main__":
    player1 = Player()
    player2 = Player()
    i = Interface()

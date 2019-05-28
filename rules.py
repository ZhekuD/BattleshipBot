class Player:
    def __init__(self):
        self.control = Control(self)
        self.field = [[0] * 10] * 10
        self.enemy_field = [[0] * 10] * 10

    @staticmethod
    def show_field(field):
        for i in field:
            print(i)


class Ship:
    def __init__(self, length):
        self.horizontal = None
        self.x = None
        self.y = None
        self.alive = True
        if 0 < length <= 4:
            self.length = length
        else:
            raise AttributeError

    def set_position(self, player, horizontal, x, y):
        self.horizontal = horizontal
        field_copy = []                         # Делаем копию поля игрока в первоначальном виде
        for i in player.field:
            field_copy.append(i.copy())

        def wrap_creator(obj, *args):
            if args[0] >= 0 and args[1] >= 0:
                try:
                    obj.field[args[0]][args[1]] = 2
                except IndexError:
                    pass

        try:
            if self.horizontal:
                for i in range(3):              # Ставим ограничитель вокруг горизонтального корабля
                    wrap_creator(player, y - 1 + i, x - 1)
                    wrap_creator(player, y - 1 + i, x + self.length)

                for i in range(self.length):
                    wrap_creator(player, y + 1, x + i)
                    wrap_creator(player, y - 1, x + i)

                for i in range(self.length):    # Ставим сам горизонтальный корабль
                    if player.field[y][x + i]:
                        raise IndexError
                    player.field[y][x + i] = 1

            else:
                for i in range(3):              # Ставим ограничитель вокруг вертикального корабля
                    wrap_creator(player, y - 1, x - 1 + i)
                    wrap_creator(player, y + self.length, x - 1 + i)

                for i in range(self.length):
                    wrap_creator(player, y + i, x - 1)
                    wrap_creator(player, y + i, x + 1)

                for i in range(self.length):    # Ставим сам вертикальный корабль
                    if player.field[y + i][x]:
                        raise IndexError
                    player.field[y + i][x] = 1

        except IndexError:                      # Если корабль не поместился - востанавливаем изначальное поле
            player.field = field_copy
            print('Error: not enough space!')
            return False

        self.x = int(x)
        self.y = int(y)
        return True


class Control:
    def __init__(self, player):
        self.player = player
        self.four_decker1 = Ship(4)
        for i in range(1, 3):
            setattr(self, f'three_decker{i}', Ship(3))
        for i in range(1, 4):
            setattr(self, f'two_decker{i}', Ship(2))
        for i in range(1, 5):
            setattr(self, f'single_decker{i}', Ship(1))

    def ships_deploy(self):
        for attr in self.__dict__:
            if isinstance(getattr(self, attr), Ship):
                result = False
                while not result:               # Цикл запусткается только если функция set_position вернула False
                    print(f'write position for {attr}:')
                    result = getattr(self, attr).set_position(
                        self.player,
                        bool(input('is it horizontal? ')),
                        int(input('x: ')),
                        int(input('y: '))
                    )

                    self.player.show_field()
                    print('\n')


if __name__ == '__main__':
    p1 = Player()
    p2 = Player()
    s = Ship(4)

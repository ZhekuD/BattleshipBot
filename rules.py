class Player:
    def __init__(self):
        self.control = Control(self)
        self.ships = Ships(self)
        self.field = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.enemy_field = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

    def show_field(self, field=True):
        a = self.field if field else self.enemy_field
        for i in a:
            print(i)


class Ship:
    def __init__(self, length):
        self.horizontal = None
        self.x = None
        self.y = None
        self.alive = True
        if 0 < length <= 4:
            self.length = length
            self.health = length

    def __repr__(self):
        return f'S{self.length}'

    def hit(self):
        self.health -= 1
        if not self.health:
            self.alive = False
            return self.alive
        return self.alive

    def set_position(self, player, horizontal, x, y):
        self.horizontal = horizontal
        field_copy = []                         # Делаем копию поля игрока в первоначальном виде
        for i in player.field:
            field_copy.append(i.copy())

        try:
            self.ship_drawing(self, player, x, y, filler=self)

        except IndexError:                      # Если корабль не поместился - востанавливаем изначальное поле
            player.field = field_copy
            print('Error: not enough space!')
            return False

        self.x = int(x)
        self.y = int(y)
        return True

    @staticmethod
    def ship_drawing(ship_obj, player, x, y, filler, attr='field', error=True):

        def wrap_creator(obj, *args):
            if args[0] >= 0 and args[1] >= 0:
                try:
                    getattr(obj, attr)[args[0]][args[1]] = 9
                except IndexError:
                    pass

        if ship_obj.horizontal:
            for i in range(3):                      # Ставим ограничитель вокруг горизонтального корабля
                wrap_creator(player, y - 1 + i, x - 1)
                wrap_creator(player, y - 1 + i, x + ship_obj.length)

            for i in range(ship_obj.length):
                wrap_creator(player, y + 1, x + i)
                wrap_creator(player, y - 1, x + i)

            for i in range(ship_obj.length):        # Ставим сам горизонтальный корабль
                if error and getattr(player, attr)[y][x + i]:
                    raise IndexError
                getattr(player, attr)[y][x + i] = filler

        else:
            for i in range(3):                      # Ставим ограничитель вокруг вертикального корабля
                wrap_creator(player, y - 1, x - 1 + i)
                wrap_creator(player, y + ship_obj.length, x - 1 + i)

            for i in range(ship_obj.length):
                wrap_creator(player, y + i, x - 1)
                wrap_creator(player, y + i, x + 1)

            for i in range(ship_obj.length):        # Ставим сам вертикальный корабль
                if error and getattr(player, attr)[y + i][x]:
                    raise IndexError
                getattr(player, attr)[y + i][x] = filler

class Ships:
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


class Control:
    def __init__(self, player):
        self.player = player

    def shoot(self, enemy, x, y):
        enemy_health = None
        if isinstance(enemy.field[y][x], Ship):
            enemy_ship = enemy.field[y][x]
            enemy_health = enemy_ship.hit()
            enemy.field[y][x] = 2
            self.player.enemy_field[y][x] = 'hit'
            print('Hit!')

            if not enemy_health:
                x, y = enemy_ship.x, enemy_ship.y
                enemy_ship.ship_drawing(
                    enemy_ship,
                    self.player,
                    x, y,
                    filler=1,
                    attr='enemy_field',
                    error=False
                )

        else:
            self.player.enemy_field[y][x] = 'miss'

        self.player.show_field(False)
        return enemy_health


if __name__ == '__main__':
    p1 = Player()
    p2 = Player()
    s = Ship(4)

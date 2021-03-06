from random import randint
from json import dumps, loads


class Player:
    def __init__(self, input_data=None):
        input_data = input_data if input_data else {}
        self.counter = 0
        self.hp = 10
        self.control = Control(self)
        self.ships = Ships(self)
        self.field = input_data.get('field') or field_factory()
        self.enemy_field = input_data.get('enemy_field') or field_factory()

    def data_output(self):
        field_data = [[str(cell) if isinstance(cell, Ship) else cell for cell in line] for line in self.field]
        enemy_filed_data = [[cell for cell in line] for line in self.enemy_field]
        ships_data = self.ships.data_output()
        player_hp = self.hp
        return dumps({
            'field': field_data,
            'enemy_field': enemy_filed_data,
            'ships_data': ships_data,
            'hp': player_hp
        })

    def data_input(self, json):
        input_dict = loads(json)
        for ship_obj in self.ships.list:
            ship_obj.__dict__ = input_dict['ships_data'][str(ship_obj)]
            ship_obj.__dict__['player'] = self
        self.hp = input_dict['hp']
        self.enemy_field = input_dict['enemy_field']
        self.field = [
            [
                tuple(filter(lambda x: str(x) == cell, self.ships.list))[0]
                if str(cell)[:1] == 'S' else cell
                for cell in line
            ]
            for line in input_dict['field']
        ]

    def data_erase(self):
        self.counter = 0
        self.hp = 10
        self.ships = Ships(self)
        self.field, self.enemy_field = field_factory(), field_factory()

    def show_field(self, field=True):
        a = self.field if field else self.enemy_field
        for i in a:
            print(i)


class Ship:
    def __init__(self, length, player):
        player.counter += 1
        self.number = player.counter
        self.player = player
        self.horizontal = None
        self.x = None
        self.y = None
        self.alive = True
        if 0 < length <= 4:
            self.length = length
            self.health = length

    def __repr__(self):
        return f'S{self.length}_{self.number}'

    def hit(self):
        self.health -= 1
        if not self.health:
            self.alive = False
            self.player.hp -= 1
            return self.alive
        return self.alive

    def set_position(self, player, horizontal, x, y):
        self.horizontal = horizontal
        field_copy = []  # Делаем копию поля игрока в первоначальном виде
        for i in player.field:
            field_copy.append(i.copy())
        try:
            ship_drawing(self, player, x, y, filler=self, wrap='8')
        except IndexError:  # Если корабль не поместился - востанавливаем изначальное поле
            player.field = field_copy
            return False

        self.x = int(x)
        self.y = int(y)
        return True


class Ships:
    def __init__(self, player):
        self.player = player
        self.list = []
        for i in range(1, 5):
            for k in range(5 - i):
                self.list.append(Ship(i, player))

    def ships_status(self):
        status = {}
        for i in range(4, 0, -1):
            counter = 0
            for ship in self.list:
                if ship.length == i and ship.alive:
                    counter += 1
            status[i] = counter
        return status

    def data_output(self):
        data = {}
        for ship in self.list:
            new_dict = ship.__dict__.copy()
            new_dict['player'] = None
            data[f'{ship}'] = new_dict
        return data

    def ships_deploy(self):
        for ship in self.list:
            result = False
            while not result:  # Цикл запусткается только если функция set_position вернула False
                print(f'write position for {ship}:')
                position = beautiful_coordinates_input()
                result = ship.set_position(self.player, *position)
            yield self.player.field

    def auto_ships_deploy(self):
        for ship in self.list:
            result = False
            while not result:
                orientation = randint(0, 1)
                limit_x = ship.length - 1 if orientation else 0  # Ограничитель для случайных чисел,
                limit_y = 0 if orientation else ship.length - 1  # что бы корабль не вылазил за поле
                x = randint(0, 9 - limit_x)
                y = randint(0, 9 - limit_y)
                result = ship.set_position(self.player, orientation, x, y)


class Control:
    def __init__(self, player):
        self.player = player

    def shoot(self, enemy, x, y):
        enemy_ship_status = None
        if self.player.enemy_field[y][x]:
            return 'Error'

        if isinstance(enemy.field[y][x], Ship):
            enemy_ship = enemy.field[y][x]
            enemy_ship_status = enemy_ship.hit()
            enemy.field[y][x] = 2
            self.player.enemy_field[y][x] = 'hit'

            if not enemy_ship_status:
                x, y = enemy_ship.x, enemy_ship.y
                ship_drawing(enemy_ship, enemy, x, y, 2, 8, 'field', False)
                ship_drawing(enemy_ship, self.player, x, y, 1, 8, 'enemy_field', False)
        else:
            enemy.field[y][x] = 'miss'
            self.player.enemy_field[y][x] = 'miss'

        return enemy_ship_status


def beautiful_coordinates_input(orientation=True, c_input=False):  # Ввод координат и проверка их валидности
    ship_orientation = None
    coordinates_pattern = {
        'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4,
        'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9
    }
    while True:
        if orientation:
            ship_orientation = bool(input('is it horizontal? '))
        coor = c_input or input('write coordinate: ')
        pattern = coordinates_pattern
        if 1 < len(coor) < 4 and coor[0].isalpha() and coor[1:].isdigit():
            x = coor[0].lower()
            y = int(coor[1:]) - 1
            if x in pattern and y in pattern.values():
                if orientation:
                    return ship_orientation, int(pattern[x]), y
                return int(pattern[x]), y
        print('Error: wrong coordinate!')


def ship_drawing(ship_obj, player, x, y, filler, wrap, field='field', error=True):

    def wrap_creator(obj, *args):
        if args[0] >= 0 and args[1] >= 0:
            try:
                getattr(obj, field)[args[0]][args[1]] = wrap
            except IndexError:
                pass

    if ship_obj.horizontal:
        for i in range(ship_obj.length):  # Ставим горизонтальный корабль
            if error and getattr(player, field)[y][x + i]:
                raise IndexError
            getattr(player, field)[y][x + i] = filler

        for i in range(3):  # Ставим ограничитель вокруг горизонтального корабля
            wrap_creator(player, y - 1 + i, x - 1)
            wrap_creator(player, y - 1 + i, x + ship_obj.length)

        for i in range(ship_obj.length):
            wrap_creator(player, y + 1, x + i)
            wrap_creator(player, y - 1, x + i)

    else:
        for i in range(ship_obj.length):  # Ставим вертикальный корабль
            if error and getattr(player, field)[y + i][x]:
                raise IndexError
            getattr(player, field)[y + i][x] = filler

        for i in range(3):  # Ставим ограничитель вокруг вертикального корабля
            wrap_creator(player, y - 1, x - 1 + i)
            wrap_creator(player, y + ship_obj.length, x - 1 + i)

        for i in range(ship_obj.length):
            wrap_creator(player, y + i, x - 1)
            wrap_creator(player, y + i, x + 1)


def field_factory():
    field = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    for i in range(9):
        field.append(field[i].copy())
    return field


def create_new_game(ai=None):
    p1 = Player()
    p2 = Player()
    if ai:
        from BattleshipGame.ai import AI
        ai = AI(p2)
        return p1, p2, ai
    return p1, p2

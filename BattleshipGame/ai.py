from random import randint, sample
from json import dumps, loads


class AI:
    def __init__(self, player):
        self.player = player
        self.memory = None
        self.success_cell = None

    def memory_output(self):
        return dumps(self.memory)

    def memory_input(self, json):
        self.memory = loads(json)

    def auto_shoot(self, enemy):
        if type(self.memory) is list:
            pass

        if self.memory:
            next_key = sample(self.memory.keys(), 1)[0]
            if not self.memory[next_key]:
                next_key = 'x' if next_key == 'y' else 'y'
            next_choice = sample(self.memory[next_key], 1)[0]
            cell_status = self.player.control.shoot(enemy, *next_choice)
            self.memory[next_key].remove(next_choice)

            if cell_status is None:
                return
            if cell_status is False:
                self.memory, self.success_cell = None, None
                return
            if cell_status is True:
                if len(self.memory) == 2:
                    self.memory.pop('y') if next_key == 'x' else self.memory.pop('x')
                x, y = next_choice
                if next_key == 'x' and x + 1 < 10 and x - 1 >= 0:
                    new_next_cell = (x + 1, y) if x > self.success_cell[0] else (x - 1, y)
                    self.memory[next_key].append(new_next_cell)
                if next_key == 'y' and y + 1 < 10 and y - 1 >= 0:
                    new_next_cell = (x, y + 1) if y > self.success_cell[1] else (x, y - 1)
                    self.memory[next_key].append(new_next_cell)
                return

        while True:
            rx = randint(0, 9)
            ry = randint(0, 9)
            cell = self.player.enemy_field[ry][rx]

            if cell == 0:
                self.success_cell = (rx, ry)
                cell_status = self.player.control.shoot(enemy, rx, ry)
                if cell_status is True:  # Если в корабль попали, но он остался жив
                    self.memory = {
                        'x': [i for i in (
                                (rx - 1, ry) if rx - 1 >= 0 and not self.player.enemy_field[ry][rx - 1] else None,
                                (rx + 1, ry) if rx + 1 <= 9 and not self.player.enemy_field[ry][rx + 1] else None
                            ) if i is not None
                        ],
                        'y': [i for i in (
                                (rx, ry - 1) if ry - 1 >= 0 and not self.player.enemy_field[ry - 1][rx] else None,
                                (rx, ry + 1) if ry + 1 <= 9 and not self.player.enemy_field[ry + 1][rx] else None
                            ) if i is not None
                        ]
                    }
                    return
                return

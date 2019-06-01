from random import randint


class AI:
    def __init__(self, player):
        self.player = player
        self.memory = None

    def shoot(self, enemy):
        while True:
            random_x = randint(0, 9)
            random_y = randint(0, 9)
            cell = self.player.enemy_field[random_y][random_x]

            if cell == 0:
                cell_status = self.player.control.shoot(enemy, random_x, random_y)
                if cell_status is True:  # Если в корабль попали, но он остался жив
                    self.memory = [i for i in (
                            (random_x - 1, random_y) if random_x - 1 >= 0 else None,
                            (random_x + 1, random_y) if random_x + 1 <= 9 else None,
                            (random_x, random_y - 1) if random_y - 1 >= 0 else None,
                            (random_x, random_y + 1) if random_y + 1 <= 9 else None
                         ) if i is not None
                    ]
                    print(self.memory)
                    return
                return
            else:
                pass

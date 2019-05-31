from BattleshipGame.rules import Player, beautiful_coordinates_input
from BattleshipGame.interface import Interface


if __name__ == '__main__':
    player1 = Player()
    player2 = Player()
    interface = Interface()

    # Запускаем создание игового поля для игрока №1
    auto = bool(input('Do you want to auto-deploying your ships? (press ENTER to skip) '))
    if not auto:
        player1_field_generator = player1.ships.ships_deploy()
        interface.field_render(player1, 'field')
        while True:
            try:
                next(player1_field_generator)
            except StopIteration:
                break
            interface.field_render(player1, 'field')
    else:
        print('Generating field for player1...')
        player1.ships.auto_ships_deploy()
        interface.field_render(player1, 'field')

    # Запускаем создание игового поля для игрока №2
    print('Generating field for player2...')
    player2.ships.auto_ships_deploy()
    interface.field_render(player2, 'field')

    while True:
        print('player1\'s shoot')
        x, y = beautiful_coordinates_input(orientation=False)
        player1.control.shoot(player2, x, y)
        player1.show_field(False)
        interface.field_render(player1, 'enemy_field')

        # print('\nplayer2\'s shoot:')
        # pass

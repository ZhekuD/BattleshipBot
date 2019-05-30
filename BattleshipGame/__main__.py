from BattleshipGame.rules import Player, Ships, Ship, Control
from BattleshipGame.interface import Interface

if __name__ == '__main__':
    player1 = Player()
    player2 = Player()
    interface = Interface()

    player1_field_generator = player1.ships.ships_deploy()

    # interface.field_render(player1, 'field')
    # while True:
    #     try:
    #         next(player1_field_generator)
    #     except StopIteration:
    #         break
    #     interface.field_render(player1, 'field')

    print('Generating field for player2...')
    player2.ships.auto_ships_deploy()
    interface.field_render(player2, 'field')

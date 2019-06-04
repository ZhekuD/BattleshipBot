from BattleshipGame.rules import Player, beautiful_coordinates_input
from BattleshipGame.interface import Interface
from BattleshipGame.ai import AI


def menu():
    def start():
        print('GAME SETTINGS:\n1. Random ships deploy\n2. Choose position manually\n3. Back')
        item2 = None
        while type(item2) != int:
            item2 = input(">> ")
            item2 = int(item2) if item2.isdigit() and item2 in '123' else print('Wrong key!')
        if item2 == 1:
            choice = True
            return choice
        if item2 == 2:
            choice = False
            return choice
        if item2 == 3:
            return menu()

    print('MENU:\n1. Start game with computer\n2. Start game with another player\n3. Info\n4. Exit')
    item = None
    while type(item) != int:
        item = input(">> ")
        item = int(item) if item.isdigit() and item in '1234' else print('Wrong key!')
    if item == 1:
        return start()
    if item == 2:
        print(r'\o/')
        return menu()
    if item == 3:
        print('\nCreated by ZhekuD')
        input('Press [ENTER] to continue...\n')
        return menu()
    if item == 4:
        print('in developing...')
        return menu()


if __name__ == '__main__':
    player1 = Player()
    player2 = Player()
    ai = AI(player2)
    interface = Interface()

    print(
        r'''
            _____        __  __  __          __    _     
           // __ )____ _/ /_/ /_/ /__  _____/ /_  (_)___ 
          // __  / __ `/ __/ __/ / _ \/ ___/ __ \/ / __ \
         // /_/ / /_/ / /_/ /_/ /  __(__  ) / / / / /_/ /
        //_____/\__,_/\__/\__/_/\___/____/_/ /_/_/ .___/  by ZhekuD.
                                                /_/      
        '''
    )
    print('='*74, '\n')

    auto = menu()

    # Запускаем создание игового поля для игрока №1
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
        interface.field_render(player1)

    # Запускаем создание игового поля для игрока №2
    print('Generating field for player2...')
    player2.ships.auto_ships_deploy()

    while True:
        # Этап стрельбы игрока
        print('player1\'s shoot...')
        result = 'Error'
        while result == 'Error':
            x, y = beautiful_coordinates_input(orientation=False)
            result = player1.control.shoot(player2, x, y)
        if not player2.hp:
            interface.field_render(player1)
            print('VICTORY!!!')
            break

        # Этап стрельбы компьютера
        print('AI\'s shoot...')
        ai.auto_shoot(player1)
        # interface.field_render(player2)

        interface.field_render(player1)

        if not player1.hp:
            print('You lose... :(\n\nEnemy field:')
            interface.field_render(player2, 'field')
            break

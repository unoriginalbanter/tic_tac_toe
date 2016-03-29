'''
Created on Mar 28, 2016
Used for near-final testing and bugfixes
@author: unoriginalbanter
'''
#!/usr/bin/local/python3.5
import random
from tic_tac_toe import engine, interface


def test_coin_toss():
    g = engine.Game()
    print("==Coin toss test==")
    for i in range(10):
        print(i,g.coin_toss(1))
    
def test_win():
    print("==Test Win==")
    print("Should print 'O'")
    g = engine.Game()
    g.board=[["X","X",3],["O","O","O"],["X",8,9]]
    print(g.check_for_end())
    
def simulate_game():
    print("==Game Sim==")
    g = interface.Interface()
    g.game.setup_game(True, 3)
    g.show_board()
    while not g.game.check_for_end():
        if (g.game.turn_no%2==1):
            g.game.player_turn(random.choice(g.game.legal))
        elif (g.game.turn_no%2==0):
            g.game.comp_turn()
        g.show_board()

    
if __name__ == "__main___":
    simulate_game()

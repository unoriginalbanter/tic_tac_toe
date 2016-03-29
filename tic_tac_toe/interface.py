'''
Created on Mar 28, 2016
Command line interface for basic app usage. The main game loop is here.
The basic flow is:
    <welcome player>
    while <keep playing>:
        <game type>
        <start game>
        while <game not over>:
            <alternate turns>
        <end game>

@author: unoriginalbanter
'''
import random
from .engine import Game

class Interface(object):
    '''These mechanics are for the final terminal interface.
    If a GUI were to be developed, it could replace this module, 
    although the primary turn-taking mechanic is located in here in
    play and session, which are easily replaceable.
    
    The code was structured this way to keep any interface interacting
    through the engine module in any way.
    '''


    def __init__(self):
        
        self.game = Game()
        self.first_game = True #flag for coin toss prompts
        self.player_name= ""
        self.keep_playing = True #flag for play again loop
        self.comp_diag = { #A little snark to lighten the day
            'won':["I knew it. First chess, then go, now tic-tac-toe.",
                    "I'm the best. It was a little unfair.",
                    ],
            'lost':["You cheated. I'm telling my dad to improve my move-"\
                      +"making algorithms!",
                    ],
            'turn':["Ok, chump. Go.", 
                "Your turn, hoo-mahn.",
                "Your turn.",
                "Just go."
                ],
            'draw':["A draw. You did better than expected.",
                ],
            'start':["Good luck, hoo-mahn.", 
                "I haven't yet been updated to reflect the current understanding"\
                    " of this game, so take it easy, ok?"],
            'quit':["Sorry you were scared and had to quit."]
            }
        
        
    def coin_toss(self):
        if self.first_game:
            print("\nI have an invisible coin to pick who goes first.")
            print("I swear, it's a perfectly good coin.")
            print("It's totally not weighted or anything.")
        else:
            print("Flip for first broski.")
        user_calls = input("Heads or tails?  \n\n(1-Heads, 2-Tails)\n::")
        if int(user_calls) not in [1,2]:
            print("\n\nWoah, heads or tails only, man.")
            self.coin_toss()
        return self.game.coin_toss(int(user_calls))
        
    def show_board(self):
        """Prints board state in a user-readable form"""
        num = len(self.game.board)*len(self.game.board)
        pad = len(str(num))
        print("Turn no: {}".format(int(self.game.turn_no)))
        print("Remaining moves: {}".format(self.game.legal))
        row_break = "_"*((len(self.game.board))*pad+(len(self.game.board)-1)) \
            +"\n"
        print(row_break.join(
            "|".join(str(ent).rjust(pad) for ent in row)+"\n" 
            for row in self.game.board)
              )
        
    def select_game(self):
        '''Returns n (where the tic tac toe board will be n by n squares long)'''
        n = input('What kind of tic tac toe game do you want to play, punkeroonie?\n'+\
            'n=? \n'+\
            '(ie., "3" if you want a classic 3x3)\n\n::'
            )
        n = int(n)
        if n < 3:
            print("That would be an unwillable game, friend.")
            self.select_game()
        else:
            print("\033c")
            print("Ok, you know the rules:\n\n{} in a row, that's how I'll win".format(
                  n
                  )
                )
        input("\n\nReady?  (press ENTER to continue)\n::")
        print("\033c")
        return n
    
    def start_game(self, coin, num):
        self.game.setup_game(coin, m=num)
        self.show_board()
        
    def play_again(self):
        '''
        Asks for user input to play again, returns bool True if yes.
        '''
        print("Care to play again?   (1:yes, 2:no)")
        res = input("::")
        if res==1:
            return True
        elif res==2:
            return False
        else:
            print("Sorry, I didn't get that.")
            self.play_again()
            
    def welcome(self):
        print("\033c")
        print("#"*50+"\nTIC-TAC-TOE by BANTER\n"+"#"*50+"\n")
        print("\n"*2)
        self.player_name=input("What is your name, Player 1?\n::")
        print("\033c")
        print("\n Hmm, I think I'll call you Player 1, {}.".format(
                self.player_name))
        print("I hope you dont mind.\n")
    
    def player_move(self):
        '''Gets player's desired move, displays turn number and current board
        state.
        '''
        print("\033c")
        print("Turn number: {}".format(str(self.game.turn_no)))
        self.show_board()
        print(random.choice(self.comp_diag['turn']))
        print("\n(Select a square to move to. (Ie., '1' for the spot marked 1)")
        mv = input("\n::")
        if (int(mv) in self.game.legal):
            return mv
        else:
            input("Invalid response. Press enter to continue.")
        
    
    def take_turn(self):
        '''Checks if it is currently the player's turn, then either prompts for
        their move, or allows the computer to take its turn.'''
        if ((self.game.p_token=="X") and (self.game.turn_no%2==1)):
            self.game.player_turn(self.player_move())
        elif (self.game.p_token=="O" and self.game.turn_no%2==0):
            self.game.player_turn(self.player_move())
        else:
            self.game.comp_turn()
    
    def end(self, winner):
        '''Provides the appropriate end game dialog when the game ends'''
        print("\033c")
        print("==Good Game==")
        self.show_board()
        print("WINNER:{}".format(winner))
        if (winner==self.game.p_token):
            print(random.choice(self.comp_diag['lost']))
        elif (winner==self.game.c_token):
            print(random.choice(self.comp_diag['won']))
        elif (winner=="Draw"):
            print(self.comp_diag['draw'])
        elif (winner=="User Quit"):
            print(self.comp_diag['quit'])
        
        
    def play(self):
        '''In game loop. Basically: while <no win condition>: <take turns>'''
        while not self.game.check_for_end():
            self.take_turn()
        self.end(self.game.check_for_end())

    def session(self):
        '''Main game loop. Welcomes player, plays game, offers for rematch.'''
        self.welcome()
        while self.keep_playing:
            _n = self.select_game()
            self.start_game(self.coin_toss(), _n)
            self.play()
            self.keep_playing=self.play_again()
            
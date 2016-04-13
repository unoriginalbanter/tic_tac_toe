'''
Created on Mar 27, 2016
The machinations of tic_tac_toe. No printing is done here, nor is any terminal
input taken here. That is left for the interface for potential expansion, and
was done intentionally.
@todo: comp_turn should incorporate the solved algorithm so that the computer
never loses.
@todo: player_turn has a bug involving mid-game quitting. Game does not exit
cleanly. This is an issue that occured during early development and a slightly
restructured flow.
@author: unoriginalbanter
'''
import random
class Game(object):
    '''Game machinery. Does not manage turn order.
    
    Methods:
     - coin_toss(user_called) tosses a coin and compares to given input returns
         a boolean
     - pos(space) returns the value of the board at the int numbered space
     - tran_move inputs the token into the space
     - legal_moves updates the inst. attr. list of legal moves self.legal
     - comp_turn makes a random legal move 
     - player_turn inputs player's move into the grid, and updates self.legal
     - setup_game resets the board, and assigns tokens and grid size as 
         specified.
     - check_for_end uses the other "check_" methods to do just that.
    '''


    def __init__(self):
        '''Constructs empty instance parameters for population and tracking:
        
        Attribues:
         -- board -- board state, 
         -- turn_no --, 
         -- human_x -- boolean of (human plays first), 
         -- c_token -- computer's token ('X' or 'Y'),
         -- p_token -- player's token ('X' or 'Y'),
         -- legal -- legal move list, 
         -- winlossdraw -- win/loss/draw for games this session [w/l/draw]
         -- quit -- player quit.
         -- coin_record -- record of coin-toss results [<human wins>,<comp wins>]
        '''
        self.board = [] #set in start_game, updated in whose_turn
        self.turn_no = 0 #updates in whose turn
        self.human_x = False #updates in start_game
        self.c_token = "" #set in start_game
        self.p_token = ""
        self.legal = [] #updates in whose_turn
        self.quit = False
        self._rows = []
        self._diags = []
        self.coin_record= [0,0]
        
    def coin_toss(self, user_called):
        '''Returns true if coin-toss was correct; 
        Also tosses coin, records result.
        
        user_called = 1 (heads) or 2 (tails)'''
        coin = random.randint(1,2)
        if coin == user_called:
            self.coin_record[0]+=1
            self.coin_record[1]+=1
            return True
        else:
            self.coin_record[1]+=1
            return False
        
    def pos(self, space):
        '''Short for position
        Takes the integer space, and returns the corresponding i,j coordinate
        '''
        n = len(self.board)
        num = int(space) - 1
        j = num % n 
        i = num // n 
        return (i, j)
                
    def val(self, space):
        '''
        Gets the value of the board at position <space>
        '''
        i,j = self.pos(space)
        return self.board[i][j]
    
    def tran_move(self, space, token):
        '''Inputs token into space. Depends: self.pos()'''
        rw, cl = self.pos(space)
        self.board[rw][cl]=token
        
    def legal_moves(self):
        '''Goes through the board, finding nontoken entries, updates the 
        self.legal tracker'''
        leg = []
        for row in self.board:
            for entry in row:
                if (entry!="X") and (entry!="O"):
                    leg.append(entry)
        self.legal = leg 
        
    def comp_turn(self):
        '''random element of legal is found, then move is made there.'''
        self.legal_moves()
        self.tran_move(
            random.choice(self.legal),
            self.c_token 
            )
        self.turn_no += 1
        self.legal_moves()
        
    def player_turn(self, move):
        '''Takes their move, checks for quitting, inputs move'''
        if (move in ["Exit", "exit", "quit", "Quit", "q", "Q", "e", "E"]):
            self.quit = True
            return 
        else:
            self.tran_move(move, self.p_token)
            self.turn_no += 1
            self.legal_moves()
        
    def setup_game(self, first, m=3):
        '''Sets initial values for each game based on queried params.'''
        self.human_x = first
        if self.human_x:
            self.c_token="O"
            self.p_token="X"
        else:
            self.c_token="X"
            self.p_token="O"
        self.turn_no = 1
        self.board = [[int(x*m + y+1) for y in range(m)] for x in range(m)]
        self.legal_moves()
    
    def check_rows(self):
        '''Checks each row for winner by checking for same entries. Returns
        the winner, or False if nothing.'''
        winner = False
        for row in self.board:
            if all(row[0]==entry for entry in row):
                winner = row[0]
        return winner
        
    def check_columns(self):
        '''Checks each column for a winner. Returns the winner, or False else.'''
        winner = False
        for j in range(len(self.board)-1): #for each column... (i,j) notation
            if all(self.board[i][j]==self.board[i+1][j] for i in range(len(self.board)-1)):
                winner=self.pos(j+1)
        return winner
        
    def check_diagonals(self):
        '''Checks diagonals for win, returns the winning token or False.'''
        n=len(self.board)
        winner=False
        if all(self.val(1)==self.val(1 + (n+1)*(i)) for i in range(n)): #topleft
            winner = self.val(1)
        elif all(self.val(n)==self.val(n + (n-1)*(i)) for i in range(n)): #topright
            winner = self.val(n)
        return winner
    
    def check_draw(self):
        '''Checks the boardstate for a draw, returns 'Draw' if so, False else,
        ONLY USE AFTER CHECKING ROWS, COLS AND DIAGS'''
        winner = False
        n = len(self.board)
        mp = n*n #m.p. = maximum position (number)
        if (self.pos(mp)=="X" or self.pos(mp)=="O"):
            winner="Draw"
        return winner
    
    def check_for_end(self):
        '''Returns a string "X", "O", or "Draw" for game end, or False for lack
        of existing win/ draw condition.

        Note: To my dismay, not the fastest way to do this. 
        Then again, performance would only matter on very impractical games of 
        Xs and Os, although it should still maintain generality for n>=3.'''
        #Check rows first, easy.
        if self.check_rows():
            return self.check_rows()
        elif self.check_columns():
            return self.check_columns()
        elif self.check_diagonals():
            return self.check_diagonals()
        elif self.check_draw():
            return self.check_draw()
        elif self.quit:
            return "User Quit"
        else:
            return False

    

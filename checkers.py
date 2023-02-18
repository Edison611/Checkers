# Python Class 2887
# Lesson 12 Problem 1
# Author: sjia (776649)

from tkinter import *

class CheckersBoard:
    '''represents a Checkers board'''

    def __init__(self):
        '''CheckersBoard()
        creates a Checkers board in the starting position'''
        self.board = {}  # dict to store position
        # create opening position
        for row in range(8):
            for column in range(8):
                coords = (row,column)
                if coords in [(5,0),(5,2),(5,4),(5,6),(6,1),(6,3),(6,5),(6,7),(7,0),(7,2),(7,4),(7,6)]:
                    self.board[coords] = 1  # player 1
                elif coords in [(0,1),(0,3),(0,5),(0,7),(1,0),(1,2),(1,4),(1,6),(2,1),(2,3),(2,5),(2,7)]:
                    self.board[coords] = 0  # player 0
                else:
                    self.board[coords] = None  # empty
        self.currentPlayer = 0  # player 0 starts
        self.endgame = None  # replace with string when game ends

    def get_piece(self,coords):
        '''CheckersBoard.get_piece(coords) -> int
        returns the piece at coords'''
        return self.board[coords]

    def get_endgame(self):
        '''CheckersBoard.get_endgame() -> None or str
        returns endgame state'''
        return self.endgame

    def get_player(self):
        '''CheckersBoard.get_player() -> int
        returns the current player'''
        return self.currentPlayer

    def next_player(self):
        '''CheckersBoard.next_player()
        advances to next player'''
        self.currentPlayer = 1 - self.currentPlayer
    
    def can_jump(self):
        '''CheckersBoard.can_jump() -> dict
        returns a dictionary of all possible jumps'''
        moves = {}  # if player can jump, the moves will be put here
        for row in range(8):  # check each square
            for column in range(8):
                coords = (row,column)
                # skips blank squares
                if self.board[coords] == None:
                    continue
                # checks if jump is outside of the board
                right_possible = False
                left_possible = False
                if column+2<8:
                    right_possible = True
                if column-2>=0:
                    left_possible = True
                # checks red pieces
                if self.currentPlayer == 0 and self.board[coords] == 0:
                    forward_possible = False
                    if row+2<8:
                        forward_possible = True
                    #checks if a jump is possible   
                    if right_possible and forward_possible:
                        if self.board[row+1,column+1] == 1 and self.board[row+2,column+2] == None:
                            # adds the two squares that can make a jump into the dictionary
                            moves[(row,column)]=(row+2,column+2)
                    if left_possible and forward_possible:
                        if self.board[row+1,column-1] == 1 and self.board[row+2,column-2] == None:
                            moves[(row,column)]=(row+2,column-2)
                            
                # checks white pieces
                if self.currentPlayer == 1 and self.board[coords] == 1:
                    forward_possible = False
                    if row-2>0:
                        forward_possible = True
                    if right_possible and forward_possible:
                        if self.board[row-1,column+1] == 0 and self.board[row-2,column+2] == None:
                            moves[(row,column)]=(row-2,column+2)
                    if left_possible and forward_possible:
                        if self.board[row-1,column-1] == 0 and self.board[row-2,column-2] == None:
                            moves[(row,column)]=(row-2,column-2)
        return moves

    def try_move(self,selected_piece,coords):
        '''CheckersBoard.try_move(coords)
        try's the move inputted by the player'''
        if self.board[coords] is not None:  # if square occupied
            return  # do nothing
        deltaX = abs(selected_piece[1]-coords[1])
        deltaY = selected_piece[0]-coords[0]

        jump = self.can_jump()
        print(jump)
        if len(jump) > 0:
            for key in jump:
                if key == selected_piece and jump[key] == coords:
                    print("yes")
                    sel_0 = selected_piece[0]
                    sel_1 = selected_piece[1]
                    coo_0 = coords[0]
                    coo_1 = coords[1]
                    deltaX = int(coo_1-sel_1)/2
                    deltaY = int(coo_0-sel_0)/2
                    self.board[coords] = self.currentPlayer
                    self.board[selected_piece[0]+deltaY,selected_piece[1]+deltaX] = None
                    self.board[coords] = self.currentPlayer
                    if len(self.can_jump()) > 0:
                        return True
                    else:
                        self.next_player()  # next player's turn
                        self.check_endgame()  # check if game over
                        return True
            else:
                print("no")
                return 
        
        if deltaX == 1 and deltaY == -1 and self.get_player()==0:
            self.board[coords] = self.currentPlayer
            self.next_player()  # next player's turn
            self.check_endgame()  # check if game over
            return True
        elif deltaX == 1 and deltaY == 1 and self.get_player()==1:
            self.board[coords] = self.currentPlayer
            self.next_player()  # next player's turn
            self.check_endgame()  # check if game over
            return True
        

    def check_endgame(self):
        '''CheckersBoard.check_endgame()
        checks if game is over'''
        # if current player has no pieces left
        p0_pieces = 0
        p1_pieces = 0
        for row in range(8):
            for column in range(8):
                coords = (row,column)
                if self.get_piece(coords) == 0:
                    p0_pieces += 1
                if self.get_piece(coords) == 1:
                    p1_pieces += 1

        if p0_pieces == 0:
            self.endgame = 1
        elif p1_pieces == 0:
            self.endgame = 0
        else:
            return

class CheckersSquare(Canvas):
    '''displays a square in the Checkers game'''

    def __init__(self,master,r,c):
        '''CheckersSquare(master,r,c)
        creates a new blank Checkers square at coordinate (r,c)'''
        # create and place the widget
        if r%2==0:
            if c%2==0:
                color = 'white'
            else:
                color = 'dark green'
        if r%2==1:
            if c%2==0:
                color = 'dark green'
            else:
                color = 'white'
        if r>8:
            Canvas.__init__(self,master,width=70,height=70,bg='light grey')
        elif color == 'dark green':
            Canvas.__init__(self,master,width=70,height=70,bg='dark green',highlightbackground='dark green')
        else:
            Canvas.__init__(self,master,width=70,height=70,bg='blanched almond',highlightbackground='blanched almond')
        self.grid(row=r,column=c)
        # set the attributes
        self.position = (r,c)
        self.isKing = False
        # bind button click to placing a piece
        self.bind('<Button>',master.get_click)

    def get_position(self):
        '''ReversiSquare.get_position() -> (int,int)
        returns (row,column) of square'''
        return self.position

    def make_color(self,color):
        '''ReversiSquare.make_color(color)
        changes color of piece on square to specified color'''
        ovalList = self.find_all()  # remove existing piece
        for oval in ovalList:
            self.delete(oval)
        self.create_oval(10,10,65,65,fill=color)

    def remove_piece(self):
        ovalList = self.find_all()  # remove existing piece
        for oval in ovalList:
            self.delete(oval)

class CheckersGame(Frame):
    '''represents a game of Reversi'''

    def __init__(self,master):
        '''ReversiGame(master)
        creates a new Reversi game'''
        # initialize the Frame
        Frame.__init__(self,master,bg='white')
        self.grid()
        # set up game data
        self.colors = ('red','white')  # players' colors
        self.piece_selected = False
        self.selected_piece = None
        # create board in starting position, player 0 going first
        self.board = CheckersBoard() 
        self.squares = {}  # stores CheckersSquares
        for row in range(8):
            for column in range(8):
                rc = (row,column)
                self.squares[rc] = CheckersSquare(self,row,column)
        # set up scoreboard and status markers
        self.rowconfigure(8,minsize=3)  # leave a little space
        self.turnSquares = []  # to store the turn indicator squares
        self.turnLabels = []  # to store the score labels
        # create indicator squares and score labels
        
        for i in range(1):  
            self.turnSquares.append(CheckersSquare(self,9,2))
            self.turnSquares[i].make_color(self.colors[0])
            self.turnSquares[i].unbind('<Button>')
            self.turnLabels.append(Label(self,text='Turn:',font=('Arial',18)))
            self.turnLabels[i].grid(row=9,column=1)
        
        self.update_display()

    def get_selectStatus(self):
        return self.piece_selected

    def get_click(self,event):
        '''CheckersGame.get_click(event)
        event handler for mouse click
        gets click data and selects the piece'''
        selected = event.widget.get_position()
        if self.get_selectStatus() == True and self.squares[selected]['bg'] == 'dark green':
            move = self.board.try_move(self.selected_piece,selected)
            if move == True:
                self.board.board[self.selected_piece] = None
                self.squares[self.selected_piece]['highlightbackground'] = 'dark green'
                self.piece_selected = False
                self.selected_piece = None
                self.update_display()
        if self.board.get_player() == self.board.board[selected]:
            if self.selected_piece != None:
                self.squares[self.selected_piece]['highlightbackground'] = 'dark green'
            self.piece_selected = True
            #self.squares[selected].piece_selected = True
            self.selected_piece = selected
            self.squares[selected]['highlightbackground'] = 'black'
            self.update_display

    def update_display(self):
        '''CheckersGame.update_display()
        updates squares to match board'''
        # update squares
        for row in range(8):
            for column in range(8):
                rc = (row,column)
                piece = self.board.get_piece(rc)
                if piece is not None:
                    self.squares[rc].make_color(self.colors[piece])
                else:
                    self.squares[rc].remove_piece()

        # update the turn indicator
        currentPlayer = self.board.get_player()
        self.turnSquares[0].make_color(self.colors[currentPlayer])
        
        # if game over, show endgame message
        endgame = self.board.get_endgame()
        if endgame is not None:  # if game is over
            # remove the turn indicator
            self.turnSquares[newPlayer]['highlightbackground'] = 'white'
            if isinstance(endgame,int):  # if a player won
                winner = self.colors[endgame]  # color of winner
                endgameMessage = '{} wins!'.format(winner.title())
            Label(self,text=endgameMessage,font=('Arial',18)).grid(row=9,column=2,columnspan=4)

# main game
def play_checkers():
    '''play_checkers()
    starts a new game of checkers'''
    root = Tk()
    root.title('Checkers')
    CheckersGame(root)
    root.mainloop()
play_checkers()

#

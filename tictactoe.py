"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[None, None, None],
            [None, None, None],
            [None, None, None]]


def player(board):
    x_count = 0
    o_count = 0
    for li in board:
        x_count += li.count(X)
        o_count += li.count(O)
    if x_count > o_count:
        return O
    return X


def actions(board):
    actions_set = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                actions_set.add((i, j))
    
    return(actions_set)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)

    try:
        i, j = action[0], action[1]
        new_board[i][j] = player(board)
    except IndexError:
        raise Exception("Action is not valid") from None

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    x_win = [X,X,X]
    o_win = [O,O,O]
    board_c = copy.deepcopy(board)

    vertical_board = [[board_c[0][0], board_c[1][0], board_c[2][0]],
                      [board_c[0][1], board_c[1][1], board_c[2][1]],
                      [board_c[0][2], board_c[1][2], board_c[2][2]]]
    diagnal_board = [[board_c[0][0], board_c[1][1], board_c[2][2]],
                     [board_c[0][2], board_c[1][1], board_c [2][0]]]
    if x_win in board+vertical_board+diagnal_board:
        return X
    elif o_win in board+vertical_board+diagnal_board:
        return O
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    plain_list = []
    for item in board:
        for sub_itme in item:
            plain_list.append(sub_itme)

    if winner(board) != None or all(item is not None for item in plain_list):
        return True
    else:
        return False
    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)

    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    class Grid():
        def __init__(self, atgh=None, layout=initial_state(), original_action = None) -> None:
            self.layout = layout
            self.terminal = terminal(layout)
            self.utility = utility(layout)
            self.player = player(layout)
            self.value = None
            self.outcams = []
            self.atgh = atgh
            self.original_action = original_action
        
        def solve(self,):
            while True:
                if self.terminal == True:
                    return (self.utility, self.atgh)
                else:
                    possible_actions = actions(self.layout)
                    for action in possible_actions:
                        if self.layout == board:
                            child = Grid(atgh=action, layout=result(self.layout, action), original_action=action)
                        else:
                            child = Grid(atgh=action, layout=result(self.layout, action), original_action=self.original_action)
                        self.outcams.append(child.solve())
                    if player(self.layout) == X:
                        if self.layout == board:
                            return max(self.outcams, key= lambda item: item[0])
                        else:
                            return (max(self.outcams, key= lambda item: item[0])[0], self.original_action)
                    if player(self.layout) == O:
                        if self.layout == board:
                            return min(self.outcams, key= lambda item: item[0])
                        else:
                            return (min(self.outcams, key= lambda item: item[0])[0], self.original_action)

    if not terminal(board):
        boar = Grid(None, board)
        return(boar.solve()[1])
    else:
        return None
    
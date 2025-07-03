"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    TicTacToe rules X always goes first, so if equal X and O in rows, its X turn.
    """
    total_X = sum(row.count(X) for row in board)
    total_O = sum(row.count(O) for row in board)
    if total_O == total_X:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Psuedo - return all rows (i) and colums (j) that are EMPTY (don't contain X or O)
    return {
        (i, j)
        for i in range(3)
        for j in range(3)
        if board[i][j] == EMPTY  # does not contain X or O
    }


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action  # action will be (row, column)

    if not (0 <= i and 0 <= j < 3) or board[i][j] is not EMPTY:
        raise Exception("Invalid move")

    next_board = [row.copy() for row in board]  # copy the current board
    next_board[i][j] = player(board)  # New board includes play action
    return next_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # ROW, requires same character in location 0, 1 and 2 of same row, or
    # COLUMN, you would have same character at location 0,1, or 2 on each row, or
    # DIAGNAL, like row 1:0, row2:1, and row 3:3 to win.

    # ROW, requires same character in location 0, 1 and 2 of same row.
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]

    # COLUMN, you would have same character at location 0,1, or 2 on each row.
    for col in range(3):
        if (
            board[0][col] == board[1][col] == board[2][col]
            and board[0][col] is not EMPTY
        ):
            return board[0][col]

    # DIAGNAL, like row 1:0, row2:1, and row 3:3 to win.
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]

    elif board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    else:
        return None  # No Winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check for Winnter: Winner is established as X or O (not None), return True (terminal)
    if winner(board) is not None:
        return True

    # Empty board function.  If there is an empty row, then False (not terminal), else True
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Game Over?
    if terminal(board):
        return None

    # Determine if AI is X or O (Maximizer or Minimizer)
    turn = player(board)

    # If AI is X and Maximizing look for open spaces adjacent to X,
    # then look to see if you could form a line or diagnal (i, j) from action
    def maximizer(state):
        if terminal(state):
            return utility(state)

        value = -2

        for action in actions(state):
            value = max(value, minimizer(result(state, action)))
        return value

    # If AI is O and Minimizin consider cost of other player.
    def minimizer(state):
        if terminal(state):
            return utility(state)

        value = 2

        for action in actions(state):
            value = min(value, maximizer(result(state, action)))
        return value

    # Determine the optimal move for optimal score
    optimal_move = None

    # If X, optimal score is -2 (-1, 0, 1 logic) maximizer
    if turn == X:
        optimal_score = -2
        for action in actions(board):
            score = minimizer(result(board, action))
            if score > optimal_score:
                optimal_score = score
                optimal_move = action

    # If O, optimal socre is 2 (-1, 0, 1 logic) for minimizer
    else:
        optimal_score = 2
        for action in actions(board):
            score = maximizer(result(board, action))
            if score < optimal_score:
                optimal_score = score
                optimal_move = action

    # Return the optimal move
    return optimal_move

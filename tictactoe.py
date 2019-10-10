"""For testing our game"""
import unittest


class TicTacToe(object):
    """For keeping and updating the board.

    Has the desk status, player turn and used cells as attributes"""

    curr_play = 0
    curr_board = [[]]
    used_cell = []

    def __init__(self):
        self.curr_board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.used_cell = []


def print_out(board):
    """Prints the board.

    Styled a bit."""
    for it_row in range(3):
        for it_col in range(3):
            if it_col == 0:
                print(" ", end='')
            print(board[it_row][it_col], end='')
            if it_col == 2:
                print(" ", end='')
            if it_col != 2:
                print(" | ", end='')
        print("")
        if it_row != 2:
            print("---+---+---")


def check_win(board):
    """Checks if there is a winner.

    Prints congrats to the winner."""
    for it_row_col in range(3):
        row_same = board[it_row_col][0] == board[it_row_col][1] == board[it_row_col][2]
        col_same = board[0][it_row_col] == board[1][it_row_col] == board[2][it_row_col]
        if row_same or col_same:
            print_out(board)
            print("First player wins!" if board[it_row_col][it_row_col] == 'X'
                  else "Second player wins!")
            return 1
    first_diag_same = board[0][0] == board[1][1] == board[2][2]
    second_diag_same = board[0][2] == board[1][1] == board[2][0]
    if first_diag_same or second_diag_same:
        print_out(board)
        print("First player wins!" if board[1][1] == 'X'
              else "Second player wins!")
        return 1
    return 0


def play(board, in_place, turn):
    """Makes a move to the input place.

    Adds 'X' or '0' to the board and checks if we have a winner"""
    board[(in_place - 1) // 3][(in_place - 1) % 3] = '0' if turn else 'X'
    return board


OUR_GAME = TicTacToe()
IS_DRAW = True
for num_move in range(9):
    print_out(OUR_GAME.curr_board)
    print("First player's turn:" if not OUR_GAME.curr_play else "Second player's turn")
    place = 0
    entered_valid = 0
    while not entered_valid:
        try:
            place = int(input())
            entered_valid = 1
        except ValueError:
            print("Please enter a valid number")
    while place in OUR_GAME.used_cell or place < 1 or place > 9:
        if place in OUR_GAME.used_cell:
            print("This cell is already used")
            place = int(input())
        else:
            print("This number of cell is not valid")
            place = int(input())
    OUR_GAME.used_cell.append(place)
    play(OUR_GAME.curr_board, place, OUR_GAME.curr_play)
    OUR_GAME.curr_play = not OUR_GAME.curr_play
    if check_win(OUR_GAME.curr_board):
        IS_DRAW = False
        break
if IS_DRAW:
    print_out(OUR_GAME.curr_board)
    print("Draw!")


class TestTicTacToeItems(unittest.TestCase):
    """Testing our game.

    Using the imported unittest."""
    def test_checkwin(self):
        """The testing function.

        Asserts check_win works correctly."""
        self.assertEqual(check_win([[1, 2, 'X'], ['0', '0', 'X'], [7, 8, 'X']]), 1)
        self.assertEqual(check_win([['X', 2, 3], ['0', 'X', 'X'], ['0', '0', 'X']]), 1)
        self.assertEqual(check_win([[1, 2, 'X'], ['0', '0', '0'], [7, 'X', 'X']]), 1)
        self.assertEqual(check_win([['0', '0', 'X'], ['0', 5, 'X'], ['0', 8, 9]]), 1)
        self.assertEqual(check_win([[1, 2, 'X'], ['0', '0', 'X'], ['X', 8, 9]]), 0)
        self.assertEqual(check_win([['0', 'X', '0'], ['0', 'X', 'X'], ['X', '0', 'X']]), 0)
        self.assertEqual(check_win([['0', 2, '0'], ['0', 'X', 'X'], ['X', 8, 'X']]), 0)
        self.assertEqual(check_win([[1, '0', 'X'], ['0', '0', 'X'], ['X', 8, '0']]), 0)
        self.assertEqual(check_win([['X', 2, 'X'], ['0', 'X', 'X'], ['0', 8, '0']]), 0)

    def test_play(self):
        """The testing function.

        Asserts play works correctly."""
        self.assertEqual(play([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 0),
                         [['X', 2, 3], [4, 5, 6], [7, 8, 9]])
        self.assertEqual(play([[1, 2, 3], ['X', 5, 6], [7, 8, 9]], 5, 1),
                         [[1, 2, 3], ['X', '0', 6], [7, 8, 9]])
        self.assertEqual(play([['X', '0', 3], [4, 5, 6], [7, 8, 9]], 8, 0),
                         [['X', '0', 3], [4, 5, 6], [7, 'X', 9]])
        self.assertEqual(play([['X', '0', 'X'], ['0', 'X', '0'], [7, 8, 9]], 7, 0),
                         [['X', '0', 'X'], ['0', 'X', '0'], ['X', 8, 9]])
        self.assertEqual(play([['X', '0', 3], [4, 5, 'X'], [7, 'X', '0']], 4, 1),
                         [['X', '0', 3], ['0', 5, 'X'], [7, 'X', '0']])
        self.assertEqual(play([[1, 'X', 3], ['0', 5, 'X'], [7, 8, 9]], 1, 1),
                         [['0', 'X', 3], ['0', 5, 'X'], [7, 8, 9]])
        self.assertEqual(play([[1, 'X', 3], ['0', 'X', 6], [7, '0', 9]], 1, 0),
                         [['X', 'X', 3], ['0', 'X', 6], [7, '0', 9]])

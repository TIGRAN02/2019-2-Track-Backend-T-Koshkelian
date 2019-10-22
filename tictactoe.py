"""For testing our game"""
import unittest


class TestTicTacToeItems(unittest.TestCase):
    """Testing our game.

    Using the imported unittest."""

    def test_checkwin(self):

        """The testing function.

        Asserts check_win works correctly."""

        for_test = TicTacToe()
        for_test.my_init([[1, 2, 'X'], ['0', '0', 'X'], [7, 8, 'X']])
        self.assertEqual(for_test.check_win(), 1)
        for_test.my_init([['X', 2, 3], ['0', 'X', 'X'], ['0', '0', 'X']])
        self.assertEqual(for_test.check_win(), 1)
        for_test.my_init([[1, 2, 'X'], ['0', '0', '0'], [7, 'X', 'X']])
        self.assertEqual(for_test.check_win(), 1)
        for_test.my_init([['0', '0', 'X'], ['0', 5, 'X'], ['0', 8, 9]])
        self.assertEqual(for_test.check_win(), 1)
        for_test.my_init([[1, 2, 'X'], ['0', '0', 'X'], ['X', 8, 9]])
        self.assertEqual(for_test.check_win(), 0)
        for_test.my_init([['0', 'X', '0'], ['0', 'X', 'X'], ['X', '0', 'X']])
        self.assertEqual(for_test.check_win(), 0)
        for_test.my_init([['0', 2, '0'], ['0', 'X', 'X'], ['X', 8, 'X']])
        self.assertEqual(for_test.check_win(), 0)
        for_test.my_init([[1, '0', 'X'], ['0', '0', 'X'], ['X', 8, '0']])
        self.assertEqual(for_test.check_win(), 0)
        for_test.my_init([['X', 2, 'X'], ['0', 'X', 'X'], ['0', 8, '0']])
        self.assertEqual(for_test.check_win(), 0)

    def test_play(self):
        """The testing function.

        Asserts play works correctly."""

        for_test = TicTacToe()
        for_test.my_init([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.assertEqual(for_test.play(1), [['X', 2, 3], [4, 5, 6], [7, 8, 9]])
        for_test.my_init([[1, 2, 3], ['X', 5, 6], [7, 8, 9]])
        self.assertEqual(for_test.play(5), [[1, 2, 3], ['X', '0', 6], [7, 8, 9]])
        for_test.my_init([['X', '0', 3], [4, 5, 6], [7, 8, 9]])
        self.assertEqual(for_test.play(8), [['X', '0', 3], [4, 5, 6], [7, 'X', 9]])
        for_test.my_init([['X', '0', 'X'], ['0', 'X', '0'], [7, 8, 9]])
        self.assertEqual(for_test.play(7), [['X', '0', 'X'], ['0', 'X', '0'], ['X', 8, 9]])
        for_test.my_init([['X', '0', 3], [4, 5, 'X'], [7, 'X', '0']])
        self.assertEqual(for_test.play(4), [['X', '0', 3], ['0', 5, 'X'], [7, 'X', '0']])
        for_test.my_init([[1, 'X', 3], ['0', 5, 'X'], [7, 8, 9]])
        self.assertEqual(for_test.play(1), [['0', 'X', 3], ['0', 5, 'X'], [7, 8, 9]])
        for_test.my_init([[1, 'X', 3], ['0', 'X', 6], [7, '0', 9]])
        self.assertEqual(for_test.play(1), [['X', 'X', 3], ['0', 'X', 6], [7, '0', 9]])


class TicTacToe:
    """For keeping and updating the board.

    Has the desk status, player turn and used cells as attributes"""

    curr_play = 0
    curr_board = [[]]
    used_cell = []

    def __init__(self):
        self.curr_board = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.used_cell = []
        self.curr_play = 0

    def my_init(self, curr_board):
        """Custom initializing function.

        Sets all the fields according to curr_board"""
        self.curr_board = curr_board
        self.curr_play = 0
        self.used_cell = []
        count_0 = 0
        count_x = 0
        for it_row in range(3):
            for it_col in range(3):
                if self.curr_board[it_row][it_col] == '0':
                    self.used_cell.append(it_row * 3 + it_col)
                    count_0 += 1
                if self.curr_board[it_row][it_col] == 'X':
                    self.used_cell.append(it_row * 3 + it_col)
                    count_x += 1
        if count_x > count_0:
            self.curr_play = 1
        else:
            self.curr_play = 0
        return self

    def print_out(self):
        """Prints the board.

        Styled a bit."""
        for it_row in range(3):
            for it_col in range(3):
                if it_col == 0:
                    print(" ", end='')
                print(self.curr_board[it_row][it_col], end='')
                if it_col == 2:
                    print(" ", end='')
                if it_col != 2:
                    print(" | ", end='')
            print("")
            if it_row != 2:
                print("---+---+---")

    def check_win(self):
        """Checks if there is a winner.

        Prints congrats to the winner."""
        for it_row_col in range(3):
            row_same = self.curr_board[it_row_col][0] == self.curr_board[it_row_col][1] == \
                       self.curr_board[it_row_col][2]
            col_same = self.curr_board[0][it_row_col] == self.curr_board[1][it_row_col] == \
                       self.curr_board[2][it_row_col]
            if row_same or col_same:
                self.print_out()
                print("First player wins!" if self.curr_board[it_row_col][it_row_col] == 'X'
                      else "Second player wins!")
                return 1
        first_diag_same = self.curr_board[0][0] == self.curr_board[1][1] == self.curr_board[2][2]
        second_diag_same = self.curr_board[0][2] == self.curr_board[1][1] == self.curr_board[2][0]
        if first_diag_same or second_diag_same:
            self.print_out()
            print("First player wins!" if self.curr_board[1][1] == 'X'
                  else "Second player wins!")
            return 1
        return 0

    def play(self, in_place):
        """Makes a move to the input place.

        Adds 'X' or '0' to the board and checks if we have a winner"""
        self.curr_board[(in_place - 1) // 3][(in_place - 1) % 3] = '0' if self.curr_play else 'X'
        return self.curr_board


OUR_GAME = TicTacToe()
IS_DRAW = True
for num_move in range(9):
    OUR_GAME.print_out()
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
            entered_valid = 0
            while not entered_valid:
                try:
                    place = int(input())
                    entered_valid = 1
                except ValueError:
                    print("Please enter a valid number")
        else:
            print("This number of cell is not valid")
            entered_valid = 0
            while not entered_valid:
                try:
                    place = int(input())
                    entered_valid = 1
                except ValueError:
                    print("Please enter a valid number")
    OUR_GAME.used_cell.append(place)
    OUR_GAME.play(place)
    OUR_GAME.curr_play = not OUR_GAME.curr_play
    if OUR_GAME.check_win():
        IS_DRAW = False
        break
if IS_DRAW:
    OUR_GAME.print_out()
    print("Draw!")

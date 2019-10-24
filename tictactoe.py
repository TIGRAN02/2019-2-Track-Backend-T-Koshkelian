"""Tictactoe game implementation.

Just for fun."""


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

    def main(self):
        """The playing.

        Main part.
        """
        is_draw = True
        for _ in range(9):
            self.print_out()
            print("First player's turn:" if not self.curr_play else "Second player's turn")
            place = 0
            entered_valid = 0
            while not entered_valid:
                try:
                    place = int(input())
                    entered_valid = 1
                except ValueError:
                    print("Please enter a valid number")
            while place in self.used_cell or place < 1 or place > 9:
                if place in self.used_cell:
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
            self.used_cell.append(place)
            self.play(place)
            self.curr_play = not self.curr_play
            if self.check_win():
                is_draw = False
                break
        if is_draw:
            self.print_out()
            print("Draw!")


if __name__ == '__main__':
    GAME = TicTacToe()
    GAME.main()

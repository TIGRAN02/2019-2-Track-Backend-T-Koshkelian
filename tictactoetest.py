"""For testing our game"""
import unittest
from tictactoe import TicTacToe


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

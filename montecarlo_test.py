import unittest
from montecarlo.montecarlo import *

class TestDie(unittest.TestCase):

    def test_change_weight_valid(self):
        die = Die(['A', 'B', 'C'])
        die.change_weight('B', 2.5)
        self.assertEqual(die.weights['B'], 2.5)

    def test_change_weight_invalid_face(self):
        die = Die(['A', 'B', 'C'])
        with self.assertRaises(ValueError):
            die.change_weight('D', 1.0)

    def test_change_weight_invalid_weight(self):
        die = Die(['A', 'B', 'C'])
        with self.assertRaises(ValueError):
            die.change_weight('B', 'two')

    def test_roll(self):
        die = Die(['A', 'B', 'C'])
        outcomes = die.roll(5)
        self.assertEqual(len(outcomes), 5)

    def test_show_faces_and_weights(self):
        die = Die(['A', 'B', 'C'])
        df = die.show_faces_and_weights()
        self.assertEqual(df.loc[df['face'] == 'B', 'weight'].values[0], 1.0)

class TestGame(unittest.TestCase):

    def test_show_results_wide(self):
        die1 = Die(['A', 'B', 'C'])
        die2 = Die(['A', 'B', 'C'])
        game = Game([die1, die2])
        game.play(3)
        df = game.show_results(form='wide')
        self.assertEqual(df.shape, (3, 2))

    def test_show_results_narrow(self):
        die1 = Die(['A', 'B', 'C'])
        die2 = Die(['A', 'B', 'C'])
        game = Game([die1, die2])
        game.play(3)
        df = game.show_results(form='narrow')
        self.assertEqual(df.shape, (6, 3))

class TestAnalyzer(unittest.TestCase):

    def test_jackpot(self):
        die1 = Die(['A', 'B', 'C'])
        die2 = Die(['A', 'B', 'C'])
        game = Game([die1, die2])
        game.play(3)
        analyzer = Analyzer(game)
        count = analyzer.jackpot()
        self.assertGreaterEqual(count, 0)

    def test_combo(self):
        die1 = Die(['A', 'B', 'C'])
        die2 = Die(['A', 'B', 'C'])
        game = Game([die1, die2])
        game.play(3)
        analyzer = Analyzer(game)
        df = analyzer.combo()
        self.assertEqual(df.shape, (2, 1))

    def test_face_counts_per_roll(self):
        die1 = Die(['A', 'B', 'C'])
        die2 = Die(['A', 'B', 'C'])
        game = Game([die1, die2])
        game.play(3)
        analyzer = Analyzer(game)
        df = analyzer.face_counts_per_roll()
        self.assertEqual(df.shape, (3, 3))

if __name__ == '__main__':
    unittest.main(verbosity=3)
import random
import pandas as pd

class Die:
    def __init__(self, faces):
        self.faces = faces
        self.weights = pd.Series([1.0] * len(faces), index=faces)

    def change_weight(self, face, weight):
        if face not in self.faces:
            raise ValueError(f"Invalid face '{face}'")
        try:
            weight = float(weight)
        except ValueError:
            raise ValueError(f"Invalid weight '{weight}'")
        self.weights[face] = weight
    
    def roll(self, times=1):
        outcomes = [random.choices(self.faces, weights=self.weights, k=1)[0] for _ in range(times)]
        return outcomes
    
    def show_faces_and_weights(self):
        return pd.DataFrame({'face': self.faces, 'weight': self.weights})

# # Create a die with faces 'A', 'B', and 'C'
# die = Die(['A', 'B', 'C'])

# # Show the die's current faces and weights
# print(die.show_faces_and_weights())

# # Change the weight of face 'B' to 2.5
# die.change_weight('B', 2.5)

# # Roll the die 5 times
# outcomes = die.roll(5)
# print(outcomes)

class Game:
    def __init__(self, dice):
        self.dice = dice
        self.results = None
    
    def play(self, times):
        rolls = [die.roll(times) for die in self.dice]
        self.results = pd.DataFrame(rolls).transpose()
        self.results.columns = range(len(self.dice))
        self.results.index.name = 'roll'
    
    def show_results(self, form='wide'):
        if form == 'wide':
            return self.results
        elif form == 'narrow':
            return pd.melt(self.results.reset_index(), id_vars=['roll'], var_name='die', value_name='face')
        else:
            raise ValueError(f"Invalid form '{form}'")

# # Create two dice with faces 'A', 'B', and 'C'
# die1 = Die(['A', 'B', 'C'])
# die2 = Die(['A', 'B', 'C'])

# # Create a game with the two dice
# game = Game([die1, die2])

# # Play the game 3 times
# game.play(3)

# # Show the results in wide form
# print(game.show_results(form='wide'))

# # Show the results in narrow form
# print(game.show_results(form='narrow'))

class Analyzer:
    def __init__(self, game):
        self.game = game
        self.dtype = type(game.dice[0].faces[0])

    def jackpot(self, face_idx=0):
        jackpot_count = (self.game.results == self.game.results.iloc[:, face_idx]).all(axis=1).sum()
        self.jackpot_results = pd.DataFrame({'Jackpot Count': jackpot_count}, index=[0])
        return jackpot_count

    def combo(self):
        combo_counts = self.game.results.apply(lambda x: len(set(x)), axis=1).value_counts().sort_index()
        combo_index = pd.MultiIndex.from_tuples([(i, ) for i in range(1, len(self.game.dice) + 1)])
        combo_results = pd.DataFrame(combo_counts, columns=['Combo Count'], index=combo_index)
        self.combo_results = combo_results
        return combo_results

    def face_counts_per_roll(self):
        num_dice = len(self.game.dice[0].faces)
        face_counts = pd.DataFrame(0, index=self.game.results.index, columns=self.game.dice[0].faces)
        for i in range(len(self.game.dice)):
            if len(self.game.dice[i].faces) != num_dice:
                raise ValueError("All dice must have the same number of faces")
            for face in self.game.dice[i].faces:
                face_counts[(i, face)] = self.game.results.iloc[:, i].apply(lambda x: x.count(face))
        self.face_counts_results = face_counts
        return face_counts


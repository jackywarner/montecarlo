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

class Analyzer:
    def __init__(self, game):
        self.game = game
        self.data_type = type(game.dice[0].faces[0])
        self.jackpot_results = None
        self.combo_results = None
        self.face_counts = None

    def jackpot(self):
        rolls = self.game.results
        n_dice = len(self.game.dice)
        jackpot_counts = 0
        for i in range(n_dice):
            first_face = self.game.dice[i].faces[0]
            mode = rolls.iloc[:, i].mode()[0]
            if mode == first_face:
                jackpot_counts += 1
        self.jackpot_results = pd.DataFrame({'jackpot_count': [jackpot_counts]}, index=[0])
        return jackpot_counts
    def combo(self):
        """
        Compute the frequency of each possible combination of faces in the rolls.
        """
        rolls = self.game.results
        combos = [tuple(sorted(set(row))) for _, row in rolls.iterrows()]
        combo_counts = pd.Series(combos).value_counts().sort_index()
        combo_index = pd.MultiIndex.from_tuples(combo_counts.index, names=['combo'])
        self.combo_results = pd.DataFrame({'combo_count': combo_counts}, index=combo_index)
        return self.combo_results

    def face_counts_per_roll(self):
        rolls = self.game.results
        face_counts = rolls.apply(pd.Series.value_counts).fillna(0).astype(int)
        face_counts.index.name = 'roll'
        self.face_counts = face_counts
        return face_counts




# A code block with your classes.
import random
import pandas as pd
class Die:
    """
    - __init__: Initializes the die with the specified faces and initializes the weights of each face to 1.0.
    - change_weight: Changes the weight of the specified face to the new weight value.
    - roll: Rolls the die the specified number of times and returns the outcomes.
    - show_faces_and_weights: Returns a pandas DataFrame containing the faces and weights of the die.
    """
    def __init__(self, faces):
        self.faces = faces  # Initialize the faces of the die
        self.weights = pd.Series([1.0] * len(faces), index=faces)  # Initialize the weights of the die to 1.0 for each face

    def change_weight(self, face, weight):
        if face not in self.faces:  # Raise ValueError if face is not one of the valid faces
            raise ValueError(f"Invalid face '{face}'")
        try:
            weight = float(weight)  # Convert weight to float if possible, otherwise raise ValueError
        except ValueError:
            raise ValueError(f"Invalid weight '{weight}'")
        self.weights[face] = weight  # Change the weight of the specified face to the new weight
    
    def roll(self, times=1):
        outcomes = [random.choices(self.faces, weights=self.weights, k=1)[0] for _ in range(times)]  # Roll the die the specified number of times and return the outcomes
        return outcomes
    
    def show_faces_and_weights(self):
        return pd.DataFrame({'face': self.faces, 'weight': self.weights})  # Return a pandas DataFrame containing the faces and weights of the die


class Game:
    """
    - __init__: Initializes the game with the specified dice and initializes the results to None.
    - play: Rolls each die in the game the specified number of times and stores the results in a pandas DataFrame.
    - show_results: Returns the results of the game in either wide or narrow format.
    """
    def __init__(self, dice):
        self.dice = dice  # Initialize the dice used in the game
        self.results = None  # Initialize the results of the game to None
    
    def play(self, times):
        rolls = [die.roll(times) for die in self.dice]  # Roll each die the specified number of times and store the outcomes in a list
        self.results = pd.DataFrame(rolls).transpose()  # Convert the list of rolls to a pandas DataFrame
        self.results.columns = range(len(self.dice))  # Rename the columns of the DataFrame to match the dice
        self.results.index.name = 'roll'  # Set the name of the index to 'roll'
    
    def show_results(self, form='wide'):
        if form == 'wide':  # Return the results in wide format
            return self.results
        elif form == 'narrow':  # Return the results in narrow format
            return pd.melt(self.results.reset_index(), id_vars=['roll'], var_name='die', value_name='face')
        else:  # Raise ValueError if the specified format is invalid
            raise ValueError(f"Invalid form '{form}'")


class Analyzer:
    """
    - __init__: Initializes the analyzer with the specified game and initializes various result attributes to None.
    - jackpot: Computes the count of jackpot wins in the game.
    - combo: Computes the frequency of each possible combination of faces in the rolls.
    - face_counts_per_roll: Computes the frequency of each face in each roll.
    """
    def __init__(self, game):
        self.game = game  # Initialize the game to be analyzed
        self.data_type = type(game.dice[0].faces[0])  # Determine the data type of the faces on the dice
        self.jackpot_results = None  # Initialize the jackpot results to None
        self.combo_results = None  # Initialize the combo results to None
        self.face_counts = None  # Initialize the face counts to None

    def jackpot(self):
        rolls = self.game.results  # Get the results of the game
        n_dice = len(self.game.dice)  # Get the number of dice in the game
        jackpot_counts = 0  # Initialize the count of jackpot wins to 0
        for i in range(n_dice):
            first_face = self.game.dice[i].faces[0]  # Get the first face of the current die
            mode = rolls.iloc[:, i].mode()[0]  # Get the mode (most frequent face) of the current die
            if mode == first_face:  # Check if the mode is the same as the first face of the die
                jackpot_counts += 1  # Increment the count of jackpot wins
        self.jackpot_results = pd.DataFrame({'jackpot_count': [jackpot_counts]}, index=[0])  # Store the jackpot results in a DataFrame
        return jackpot_counts  # Return the count of jackpot wins

    def combo(self):
        """
        Compute the frequency of each possible combination of faces in the rolls.
        """
        rolls = self.game.results  # Get the results of the game
        combos = [tuple(sorted(set(row))) for _, row in rolls.iterrows()]  # Compute the combinations of faces in each roll
        combo_counts = pd.Series(combos).value_counts().sort_index()  # Count the frequency of each combination
        combo_index = pd.MultiIndex.from_tuples(combo_counts.index, names=['combo'])  # Create a multi-level index for the combination counts
        self.combo_results = pd.DataFrame({'combo_count': combo_counts}, index=combo_index)  # Store the combo results in a DataFrame
        return self.combo_results  # Return the combo results

    def face_counts_per_roll(self):
        rolls = self.game.results  # Get the results of the game
        face_counts = rolls.apply(pd.Series.value_counts).fillna(0).astype(int)  # Count the frequency of each face in each roll
        face_counts.index.name = 'roll'  # Set the name of the index to 'roll'
        self.face_counts = face_counts  # Store the face counts in a DataFrame
        return face_counts  # Return the face counts per roll

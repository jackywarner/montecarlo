# Metadata
##### Author: Jack Warner
##### Project Name: Monte Carlo

# Synopsis 
#### Installing 
The package can be installed using pip:
```bash
!pip install git+https://github.com/jackywarner/montecarlo.git
```
#### Importing
Once installed, the package can be imported in a Python script or notebook:
```python
from montecarlo.montecarlo import Die, Game, Analyzer
```
#### Creating Dice
Dice can be created using the Die class. The faces of the die can be specified as a list of any hashable data type, and weights can be assigned to each face to adjust the probability of rolling that face. Here is an example of creating a six-sided die with equal probabilities for each face:
```python
die = Die(['1', '2', '3', '4', '5', '6'])
```
Weights can be adjusted using the change_weight method:
```python
die.change_weight(face=1, weight=2.0)
```

#### Playing games
Games can be played using the Game class. The Game class takes a list of dice as an argument. Here is an example of playing a game with two six-sided dice:
```python
dice = [Die(faces=[1, 2, 3, 4, 5, 6]), Die(faces=[1, 2, 3, 4, 5, 6])]
game = Game(dice=dice)
game.play(times=10)
```
#### Analyzing games
Game results can be analyzed using the Analyzer class. The Analyzer class takes a Game object as an argument. Here is an example of analyzing the results of a game:

```python
analyzer = Analyzer(game=game)
jackpot_counts = analyzer.jackpot()
combo_results = analyzer.combo()
face_counts = analyzer.face_counts_per_roll()
```
The jackpot method calculates the number of times that each die in the game rolls its first face. The combo method calculates the frequency of each possible combination of faces in the rolls. The face_counts_per_roll method calculates the number of times each face appears on each roll.

API description:
The package contains the following classes and methods:

class Die:

    __init__(self, faces): Creates a new Die object with the specified faces and equal weights.
    change_weight(self, face, weight): Changes the weight of the specified face.
    roll(self, times=1): Rolls the die the specified number of times and returns the outcomes.
    show_faces_and_weights(self): Returns a DataFrame showing the faces and weights of the die.

class Game:

    __init__(self, dice): Creates a new Game object with the specified dice.
    play(self, times): Plays the game the specified number of times and stores the results in a DataFrame.
    show_results(self, form='wide'): Returns the game results in either wide or narrow format.

class Analyzer:

    __init__(self, game): Creates a new Analyzer object with the specified game.
    jackpot(self): Calculates the number of times each die in the game rolls its first face and returns the results.
    combo(self): Calculates the frequency of each possible combination of faces in the game results and returns the results.
    `face_counts_per_roll











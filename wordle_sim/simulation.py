from typing import List, Tuple, Set
import string
import pandas as pd
from nltk.corpus import words
import numpy as np

def initialize_corpus():
    words_pd = pd.DataFrame()
    words_pd['word'] = words.words()
    words_pd['word'] = words_pd['word'].map(str.lower)
    words_pd = words_pd.drop_duplicates('word')
    words_pd['length'] = words_pd['word'].map(len)
    words_pd = words_pd[words_pd['length'] == 5]
    return words_pd

def initialize_letterbank():
    return [list(string.ascii_lowercase)] * 5

def check_guess(letterbank: List[List[str]], guess: str, correct_word: str) -> List[List[str]]:
    colors = []
    for index, char_ in enumerate(guess):
        if char_ == correct_word[index]:
            letterbank[index] = [char_]
            colors.append('green')
        elif char_ in correct_word:
            buffer = letterbank[index][:]
            buffer.remove(char_)
            letterbank[index] = buffer
            colors.append('yellow')
        else:
            for i in range(len(guess)):
                if char_ not in letterbank[i][:]:
                    continue
                letterbank[i].remove(char_)
            colors.append('grey')
    return letterbank, colors

def is_suitable(word: str, letterbank: List[List[str]], yellow_letters: Set[str]) -> bool:
    for index, char_ in enumerate(word):
        if not char_ in letterbank[index]:
            return False
    for letter in yellow_letters:
        if not letter in word:
            return False

    return True

def get_suitable_guesses(letterbank: List[List[str]], wordbank: pd.DataFrame, yellow_letters: List[str]):
    wordbank['is_suitable'] = wordbank['word'].apply(is_suitable, letterbank=letterbank, 
                                                     yellow_letters = yellow_letters)
    wordbank = wordbank[wordbank['is_suitable']]
    return list(wordbank['word'])

get_yellow_letters = (
    lambda letters_with_colors : [letter for letter, color in letters_with_colors.items() if color == 'yellow']
)

def simulate() -> Tuple[str, List[str], int, bool]:
    letterbank = initialize_letterbank()
    wordbank = initialize_corpus()
    correct_word = wordbank.sample(1).reset_index().loc[0,'word']
    guesses = []
    yellow_letters = set()

    for round in range(6):
        choices = get_suitable_guesses(letterbank, wordbank, yellow_letters)
        guess = np.random.choice(choices)
        guesses.append(guess)
        letterbank, colors = check_guess(letterbank, guess, correct_word)
        letters_with_colors = dict(zip(list(guess), colors))
        new_yellow_letters = get_yellow_letters(letters_with_colors)
        yellow_letters.update(set(new_yellow_letters))
        if guess == correct_word:
            return correct_word, guesses, round + 1, True

    return correct_word, guesses, 6, False
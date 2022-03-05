from typing import List, Tuple
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

is_suitable = lambda word, letterbank: all([char_ in letterbank[index] for index, char_ in enumerate(word)])  
def get_suitable_guesses(letterbank: List[List[str]], wordbank: pd.DataFrame):
    wordbank['is_suitable'] = wordbank['word'].apply(is_suitable, letterbank=letterbank)
    wordbank = wordbank[wordbank['is_suitable']]
    return list(wordbank['word'])

def simulate() -> Tuple[str, List[str], int, bool]:
    letterbank = initialize_letterbank()
    wordbank = initialize_corpus()
    correct_word = wordbank.sample(1).reset_index().loc[0,'word']
    guesses = []

    for round in range(6):
        choices = get_suitable_guesses(letterbank, wordbank)
        guess = np.random.choice(choices)
        guesses.append(guess)
        letterbank, colors = check_guess(letterbank, guess, correct_word)
        if guess == correct_word:
            return correct_word, guesses, round + 1, True

    return correct_word, guesses, 6, False
from copy import deepcopy
from typing import Dict, List, Optional, Tuple, Set
import string
import pandas as pd
from nltk.corpus import words
import numpy as np
from collections import Counter, defaultdict

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

def initialize_keyboard() -> Dict[str, str]:
    english_alphabet = list(string.ascii_lowercase)
    return {letter: 'white' for letter in english_alphabet}

def check_guess(letterbank: List[List[str]], guess: str, correct_word: str) -> List[List[str]]:
    colors = []
    counts_correct_word = Counter(correct_word)
    counts_guess = defaultdict(int)
    for index, char_ in enumerate(guess):
        counts_guess[char_] += 1
        if char_ == correct_word[index]:
            letterbank[index] = [char_]
            colors.append('green')
        elif char_ in correct_word:
            buffer = letterbank[index][:]
            buffer.remove(char_)
            letterbank[index] = buffer
            if counts_correct_word[char_] >= counts_guess[char_]:
                colors.append('yellow')
            else:
                colors.append('grey')
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

def simulate(correct_word: Optional[str] = None, 
             initial_guess: Optional[str] = None) -> Tuple[str, List[str], int, bool]:
    
    wordbank = initialize_corpus()
    
    # Check if the user provided valid values for the inital guess and correct word
    if correct_word and correct_word not in wordbank['word'].values:
        raise ValueError('The correct word has to be in the corpus')
    
    if initial_guess and initial_guess not in wordbank['word'].values:
        raise ValueError('The initial guess has to be in the corpus')

    letterbank = initialize_letterbank()
    keyboard = initialize_keyboard()

    if not correct_word:
        correct_word = wordbank.sample(1).reset_index().loc[0,'word']
    guesses = []
    yellow_letters = set()
    letterbanks = [deepcopy(letterbank)]
    keyboards = [deepcopy(keyboard)]

    for round in range(6):
        if round == 0 and initial_guess:
            guess = initial_guess
            guesses.append(guess)
        else:
            choices = get_suitable_guesses(letterbank, wordbank, yellow_letters)
            guess = np.random.choice(choices)
            guesses.append(guess)

        letterbank, colors = check_guess(letterbank, guess, correct_word)
        letters_with_colors = dict(zip(list(guess), colors))
        
        letterbanks.append(deepcopy(letterbank))
        keyboard.update(letters_with_colors)
        keyboards.append(deepcopy(keyboard))
        
        new_yellow_letters = get_yellow_letters(letters_with_colors)
        yellow_letters.update(set(new_yellow_letters))
        if guess == correct_word:
            return correct_word, guesses, round + 1, True, letterbanks, keyboards

    return correct_word, guesses, 6, False, letterbanks, keyboards
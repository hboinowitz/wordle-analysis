from typing import Dict, List
from flask import Flask
from flask import render_template
from wordle_sim import simulate

app = Flask(__name__)

def get_colors_for_guesses(guesses: List[str], keyboards: List[Dict[str, str]]):
    colors_for_guesses = []
    for round, guess in enumerate(guesses):
        colors_for_guess = []
        for char_ in guess:
            colors_for_guess.append(keyboards[round + 1][char_])
        colors_for_guesses.append(colors_for_guess[:])
    return colors_for_guesses
            
@app.route("/")
def home():
    correct_word, guesses, rounds, won, letterbanks, keyboards = simulate()
    colors_for_guesses = get_colors_for_guesses(guesses, keyboards)
    len_guesses_prior = len(guesses)
    if len_guesses_prior != 6:
        guesses.extend([[" "] * 5] * (6 - len_guesses_prior))
        colors_for_guesses.extend([["white"] * 5] * (6 - len_guesses_prior))
    print(colors_for_guesses, len(guesses))

    return render_template('base.html', guesses = guesses, correct_word = correct_word,
                           colors_for_guesses=colors_for_guesses)

if __name__ == '__main__':
    app.run(debug=True)
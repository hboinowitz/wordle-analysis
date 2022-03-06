from flask import Flask
from flask import render_template
from wordle_sim import simulate

app = Flask(__name__)

@app.route("/")
def home():
    correct_word, guesses, rounds, won, letterbanks, keyboards = simulate()
    if len(guesses) != 6:
        guesses.extend([[' '] * 5] * (6 - len(guesses)))
    return render_template('base.html', guesses = guesses, correct_word = correct_word)

if __name__ == '__main__':
    app.run(debug=True)
# Wordle-Analysis
There has been a big hype around the NY Times' word guessing game wordle recently.

In this repo I investigated how wordle works from a Data Scientific point of view by 
- some Explorative Data Analysis (EDA), researching if the length of the words (5 letters) has an impact how 'solvable' the wordle is theoretically 
- a simulation, in which a computer solves wordles
- interpreting and visualizing the simulation results
- showing a live-simulation in a dashboard app with the wordle design

## Installation
1. Clone the repo
2. Run `make install` at the root of your
local repository
3. If you have not downloaded the nltk-corpus
of english words, than you want to run
    ```py
    import nltk
    nltk.download('words')
    ```
    before jumping into the notebooks.

# Renato's Communication Game Implementation

This project implements a solution to Renato's communication game (see for example https://qid.ethz.ch/hackathon/). On top of that, it also implements a solution to a more general problem where the players are allowed to communicate 2 * k classical bits and are asked to determine the sum modulo 2^k.

## How to run
The cirq library is required.
The fully tested programs are powerTwoGame.py and powerTwoAccel.py. Both implement the game with 2 * k bits per player to tell the sum modulo 2^k with a variable number of players (n) and a variable k. Both powerTwoGame.py and powerTwoAccel.py are run in exactly the same way and their output is very similar.

run

```bash
python powerTwoGame.py
```

to run the game with default parameters (n = 2, k = 3)


run

```bash
python powerTwoGame.py n k
```

where n and k are appropriate integers to be used as the number of players and the exponent in the modulus for the game

run

```bash
python powerTwoGame.py [-s] [-c] n k
```

to optionally also print information about the state of the qubits throughout the procedure (-s) or to print what exactly are the bits the players exchange (-c)

## powerTwoGame.py vs. powerTwoAccel.py

powerTwoGame.py keeps the state of all qubits throughout the process, powerTwoAccel.py only uses as many qubits as are needed at any given point of time. Thus, powerTwoAccel.py is (for larger n) much more time- and space-efficient than powerTwoGame.py.

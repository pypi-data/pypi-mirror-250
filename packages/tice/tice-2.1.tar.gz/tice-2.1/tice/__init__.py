'''
Tic-Tac-Toe

1 | 2 | 3
4 | 5 | 6
7 | 8 | 9

```python
# Player types:
tice.player
tice.ai
tice.random
tice.dumb # less smart ai
```

# How to play:
```python
tice.game(tice.player, tice.ai).play(clear=True) # clear console if after each guess?

tice.game(tice.dumb, tice.ai).play()

tice.game(tice.player, tice.random).play()

tice.game(tice.dumb, tice.random).play()

tice.game(tice.player, tice.dumb).play()

tice.game(tice.dumb, tice.dumb).play()

tice.game(tice.random, tice.random).play()

tice.game(tice.ai, tice.ai).play()

tice.game(tice.random, tice.ai).play()

tice.game(tice.player, tice.player).play()
```
'''

import os
import random as _random_

class board(object):
    def __init__(self):
        self.b: dict = {
            1: ' ', 2: ' ', 3: ' ',
            4: ' ', 5: ' ', 6: ' ',
            7: ' ', 8: ' ', 9: ' '
        }

    def __str__(self):
        return f' {self.b[1]} | {self.b[2]} | {self.b[3]} \n-----------\n {self.b[4]} | {self.b[5]} | {self.b[6]} \n-----------\n {self.b[7]} | {self.b[8]} | {self.b[9]} '

    def display(self):
        print(self.__str__())

    def update(self, pos, player):
        if self.b[pos] != ' ':
            return False
        self.b[pos] = player
        return True

    def check(self, pos, player):
        if self.b[pos] != ' ':
            return False
        return True

    def check_draw(self):
        if ' ' not in self.b.values():
            return True
        else:
            return False

    def check_win(self):
        if self.b[1] == self.b[2] == self.b[3] != ' ':
            self.winner = self.b[1]
            return True
        elif self.b[4] == self.b[5] == self.b[6] != ' ':
            self.winner = self.b[4]
            return True
        elif self.b[7] == self.b[8] == self.b[9] != ' ':
            self.winner = self.b[7]
            return True
        elif self.b[1] == self.b[4] == self.b[7] != ' ':
            self.winner = self.b[1]
            return True
        elif self.b[2] == self.b[5] == self.b[8] != ' ':
            self.winner = self.b[2]
            return True
        elif self.b[3] == self.b[6] == self.b[9] != ' ':
            self.winner = self.b[3]
            return True
        elif self.b[1] == self.b[5] == self.b[9] != ' ':
            self.winner = self.b[1]
            return True
        elif self.b[3] == self.b[5] == self.b[7] != ' ':
            self.winner = self.b[3]
            return True
        else:
            return False

    def reset(self):
        self.b: dict = {
            1: ' ', 2: ' ', 3: ' ',
            4: ' ', 5: ' ', 6: ' ',
            7: ' ', 8: ' ', 9: ' '
        }

    @property
    def game(self):
        return self.b

    @property
    def string(self):
        return self.__str__()

    @property
    def print(self):
        return self.display()

class player(object):
    def __init__(self, board: board, player: str):
        self.b: board = board
        self.p: str = player

    def move(self):
        while True:
            try:
                pos = int(input(f'Player {self.p} move: '))
                if pos not in range(1, 10):
                    raise ValueError
                if self.b.update(pos, self.p):
                    break
                else:
                    print('Spot taken')
            except ValueError:
                print('Invalid move(1-9)')

    @property
    def game(self):
        return self.b.b

    @property
    def string(self):
        return self.b.__str__()

    @property
    def print(self):
        return self.b.display()

class ai(object):
    def __init__(self, board: board, player: str, depth: int = 5):
        self.b: board = board
        self.p: str = player
        self.max_depth = depth

    def move(self):
        best_score = float('-inf')
        best_move = None

        for move in self.b.b.keys():
            if self.b.check(move, ' '):
                board_copy = self.b.__class__()
                board_copy.b = self.b.b.copy()
                board_copy.update(move, self.p)
                score = self.minimax(board_copy, False, 0, float('-inf'), float('inf'))

                if score > best_score:
                    best_score = score
                    best_move = move

        self.b.update(best_move, self.p)

    def minimax(self, board, is_maximizing, depth, alpha, beta):
        if board.check_win():
            if board.winner == self.p:
                return 1
            else:
                return -1
        elif board.check_draw():
            return 0
        elif depth == self.max_depth:
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for move in board.b.keys():
                if board.check(move, ' '):
                    board_copy = board.__class__()
                    board_copy.b = board.b.copy()
                    board_copy.update(move, self.p)
                    score = self.minimax(board_copy, False, depth + 1, alpha, beta)
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
            return best_score
        else:
            best_score = float('inf')
            for move in board.b.keys():
                if board.check(move, ' '):
                    board_copy = board.__class__()
                    board_copy.b = board.b.copy()
                    board_copy.update(move, self.get_opponent())
                    score = self.minimax(board_copy, True, depth + 1, alpha, beta)
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
            return best_score

    def get_opponent(self):
        if self.p == 'X':
            return 'O'
        else:
            return 'X'

class random(object):
    def __init__(self, board: board, player: str):
        self.b: board = board
        self.p: str = player

    def move(self):
        while True:
            pos = _random_.randint(1, 9)
            if self.b.check(pos, ' '):
                self.b.update(pos, self.p)
                break

class game(object):
    def __init__(self, player1: player, player2: player):
        self.b: board = board()
        self.p1: player = player1(self.b, 'X')
        self.p2: player = player2(self.b, 'O')
        self.winner: str = None

    def play(self, clear=True):
        while True:
            self.b.print
            print(f'Player {self.p1.p} turn')
            self.p1.move()

            if self.b.check_win():
                self.winner = self.p1.p
                break
            elif self.b.check_draw():
                break

            if clear: os.system('clear')

            self.b.print
            print(f'Player {self.p2.p} turn')
            self.p2.move()

            if self.b.check_win():
                self.winner = self.p2.p
                break
            elif self.b.check_draw():
                break

            if clear: os.system('clear')

        print(f'Player {self.winner} won!')
        self.b.print
        self.b.reset()

class dumb(object):
    def __init__(self, board: board, player: str):
        self.b: board = board
        self.p: str = player
        self.random = random(self.b, self.p)
        self.ai = ai(self.b, self.p)

    def move(self):
        rand = _random_.randint(1, 6)
        mode = self.random if rand < 3 else self.ai
        mode.move()
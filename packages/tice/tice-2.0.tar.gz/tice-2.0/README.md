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
tice.game(board(), player, ai).play(clear=True) # clear console if after each guess?

tice.game(board(), dumb, ai).play()

tice.game(board(), player, random).play()

tice.game(board(), dumb, random).play()

tice.game(board(), player, dumb).play()

tice.game(board(), dumb, dumb).play()

tice.game(board(), random, random).play()

tice.game(board(), ai, ai).play()

tice.game(board(), random, ai).play()

tice.game(board(), player, player).play()
```
'''
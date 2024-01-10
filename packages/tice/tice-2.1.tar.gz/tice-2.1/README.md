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
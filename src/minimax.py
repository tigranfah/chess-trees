import math
from copy import deepcopy
from typing import Tuple
from utils import Action
import sys
import time
from functools import cache

sys.setrecursionlimit(100000000)


def minimax(game, depth=math.inf):
    stime = time.time()
    ret = rec_minimax(game, depth)
    print(f"minimax took {time.time() - stime:.4f}s")
    return ret


@cache
def rec_minimax(game, depth) -> Tuple[float, Action]:
    if depth == 0 or game.is_terminal():
        return game.utility(), None
    
    if game.to_move():
        highest_action_value = -math.inf
        best_action = None
        for a in game.actions():
            game_copy = game.copy()
            game_copy.perform_action(a)
            value, _ = rec_minimax(game_copy, depth - 1)
            if highest_action_value < value:
                highest_action_value = value
                best_action = a
        return highest_action_value, best_action
    else:
        lowest_action_value = math.inf
        best_action = None
        for a in game.actions():
            game_copy = game.copy()
            game_copy.perform_action(a)
            value, _ = rec_minimax(game_copy, depth - 1)
            if lowest_action_value > value:
                lowest_action_value = value
                best_action = a
        return lowest_action_value, best_action

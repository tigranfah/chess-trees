import math
from copy import deepcopy
from typing import Tuple, Dict
from utils import Action
import sys
import time
from utils import BaseGame

sys.setrecursionlimit(100000000)

look_up_dict: Dict[BaseGame, float] = {}


def minimax(game, depth=math.inf):
    stime = time.time()
    print(f"running minimax with depth {depth}")
    ret = rec_minimax(game, alpha=-math.inf, beta=math.inf, depth=depth)
    print(f"minimax took {time.time() - stime:.4f}s")
    return ret


def rec_minimax(game, alpha, beta, depth) -> Tuple[float, Action]:
    global look_up_dict
    if look_up_dict.get(game):
        return look_up_dict[game]
    if depth == 0 or game.is_terminal():
        return game.utility(), None
    
    if game.to_move():
        highest_action_value = -math.inf
        best_action = None
        for a in game.actions():
            game_copy = game.copy()
            game_copy.perform_action(a)
            value, _ = rec_minimax(game_copy, alpha, beta, depth - 1)
            if highest_action_value < value:
                highest_action_value = value
                best_action = a
                alpha = max(alpha, value)
            if value > beta:
                return value, a
        return highest_action_value, best_action
    else:
        lowest_action_value = math.inf
        best_action = None
        for a in game.actions():
            game_copy = game.copy()
            game_copy.perform_action(a)
            value, _ = rec_minimax(game_copy, alpha, beta, depth - 1)
            if lowest_action_value > value:
                lowest_action_value = value
                best_action = a
                beta = min(beta, value)
            if value < alpha:
                return value, a
        return lowest_action_value, best_action
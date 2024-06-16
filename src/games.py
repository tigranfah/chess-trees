from typing import List, Tuple
from dataclasses import dataclass
from utils import BaseGame, Action
from copy import deepcopy
from chess import Board, Move
import chess

from minimax import minimax


# Piece values
PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0  # King value is typically not included
}


class ChessGame(Board, BaseGame):

    def actions(self):
        return self.legal_moves
    
    def perform_action(self, action):
        self.push(action)
    
    def utility(self):
        score = 0
        for piece in self.piece_map().values():
            value = PIECE_VALUES[piece.piece_type]
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value
        return score
    
    def to_move(self):
        return self.turn

    def is_terminal(self):
        return self.is_game_over()
    
    def __hash__(self):
        return hash(str(self) + str(self.to_move()))


@dataclass
class TicTacToeAction(Action):
    pos: Tuple[int]
    player: str


@dataclass
class TicTacToe(BaseGame):
    grid = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]
    player = "x"
    
    def __check_rows_cols(self):
        for i in range(len(self.grid)):
            row_winner = True
            col_winner = True
            for j in range(len(self.grid) - 1):
                if self.grid[i][j] != self.grid[i][j + 1]:
                    row_winner = False

                if self.grid[j][i] != self.grid[j + 1][i]:
                    col_winner = False

            if row_winner:
                return self.grid[i][0]
            
            if col_winner:
                return self.grid[0][i]
        return None
    
    def __check_diags(self):
        diag_winner = True
        for i in range(len(self.grid) - 1):
            if self.grid[i][i] != self.grid[i + 1][i + 1]:
                diag_winner = False

        if diag_winner:
            return self.grid[0][0]
        
        diag_winner = True
        for i in range(len(self.grid) - 1):
            ind = len(self.grid) - i - 1
            if self.grid[i][ind] != self.grid[i + 1][ind - 1]:
                diag_winner = False

        if diag_winner:
            return self.grid[0][len(self.grid) - 1]
        return None
    
    def utility(self) -> float:
        winner_player = self.__check_rows_cols()
        if winner_player is None:
            winner_player = self.__check_diags()

        if winner_player == "x":
            return 1
        elif winner_player == "o":
            return -1
        return 0
    
    def perform_action(self, action: TicTacToeAction):
        assert self.grid[action.pos[0]][action.pos[1]] == " "
        self.grid[action.pos[0]][action.pos[1]] = action.player

        self.player = "o" if self.player == "x" else "x"

    def actions(self) -> List[TicTacToeAction]:
        moves = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == " ":
                    moves.append(TicTacToeAction(pos=(i, j), player=self.player))
        return moves
    
    def copy(self):
        deep_copy = TicTacToe()
        deep_copy.grid = deepcopy(self.grid)
        deep_copy.player = self.player
        return deep_copy

    def to_move(self):
        return self.player == "x"

    def is_terminal(self) -> bool:
        return len(self.actions()) == 0
    
    def __hash__(self):
        return hash("".join(["".join(a) for a in self.grid]) + self.player)
                    
    def __str__(self):
        str_repr = ""
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                str_repr += self.grid[i][j]
                if j != len(self.grid[j]) - 1:
                    str_repr += "|"
            str_repr += "\n"
            if i != len(self.grid[i]) - 1:
                str_repr += len(self.grid[i]) * "- "
                str_repr += "\n"
        return str_repr
    
    def __repr__(self):
        return str(self)
    

if __name__ == "__main__":
    cgame = ChessGame()

    while not cgame.is_terminal():
        action = None
        while action is None:
            try:
                inp = input()
                action = Move.from_uci(inp)
            except:
                print("what?")
        
        cgame.perform_action(action)
        v, a = minimax(cgame, depth=4)
        print(f"Found value {v}, action {a}")
        cgame.perform_action(a)
        print(cgame)
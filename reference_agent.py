import numpy as np
import random
from agent import Agent
from board import Board

class ReferenceAgent(Agent):
    def __init__(self, symbol, model_data: dict):
        self._symbol = symbol
        self._model_data = model_data
        
    def select_action(self, board: Board):
        board_tuple = self._board_to_tuple(board)
        
        if board_tuple not in self._model_data:
            valid_moves = board.valid_moves()
            return random.choice(valid_moves) if valid_moves else None

        action_probs = self._model_data[board_tuple]
        
        valid_moves_linear = [y * 3 + x for x, y in board.valid_moves()]
        
        chosen_relative_index = np.argmax(action_probs)
        
        chosen_absolute_index = valid_moves_linear[chosen_relative_index]
        
        return (chosen_absolute_index % 3, chosen_absolute_index // 3)

    def _board_to_tuple(self, board: Board):
        mapping = {None: 0, ' ': 0, 'X': 1, 'O': 2}
        flat_list = []
        for row in board._board: 
            for cell in row:
                flat_list.append(mapping.get(cell, 0))
        return tuple(flat_list)
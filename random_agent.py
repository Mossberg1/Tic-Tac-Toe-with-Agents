import random
from agent import Agent
from board import Board


class RandomAgent(Agent):
    def __init__(self, symbol):
        self._symbol = symbol
        
    
    def select_action(self, board: Board):  
        moves = board.valid_moves()
        return random.choice(moves) if moves else None
import pandas as pd
import numpy as np
import random
import pickle
from agent import Agent 
from board import Board
from collections import defaultdict


class QLearnAgent(Agent):
    def __init__(self, symbol, learning_rate, discount_factor, exploration_rate):
        self._symbol = symbol
        self._learning_rate = learning_rate
        self._discount_factor = discount_factor
        self._exploration_rate = exploration_rate
        self._q_table = defaultdict(lambda: np.zeros(9))
    
    
    def save_model(self, filename: str):
        data = dict(self._q_table)
        
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
        
        print(f'Model saved to: {filename}')
        
    
    def select_action(self, board: Board):
        state_key = str(board)
        
        valid_moves = board.valid_moves()
        valid_indicies = [y * 3 + x for x, y in valid_moves]
        
        if random.random() < self._exploration_rate:
            return random.choice(valid_moves)
        
        q_values = self._q_table[state_key]
        
        if np.all(q_values[valid_indicies] == 0):
            return random.choice(valid_moves)
        
        best_move_index = valid_indicies[np.argmax(q_values[valid_indicies])]
        
        return (best_move_index % 3, best_move_index // 3)
    
    
    def learn(self, state: Board, action, reward, next_state: Board):
        state_key, next_state_key = str(state), str(next_state)
        action_index = action[1] * 3 + action[0]
        
        best_next_q = np.max(self._q_table[next_state_key])
        current_q = self._q_table[state_key][action_index]
        
        self._q_table[state_key][action_index] += self._learning_rate * (reward + self._discount_factor * best_next_q - current_q)
    
    
    def load_model(self, filename: str):
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                self._q_table.update(data)
        except FileNotFoundError:
            print(f'File {filename} not found.')
    
        
    def _ensure_state(self, state_key):
        if state_key not in self._q_table:
            self._q_table[state_key] = np.zeros(9)

            
    
    
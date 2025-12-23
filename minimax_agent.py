from agent import Agent
from board import Board

class MinimaxAgent(Agent):
    def __init__(self, symbol):
        self._symbol = symbol    
        self._opponent = 'O' if symbol == 'X' else 'X'
    
    def select_action(self, board: Board) -> tuple[int, int]:
        best_score = float('-inf')
        best_move = None
        
        for move in board.valid_moves():
            x, y = move
            new_board = board.simulate_move(x, y, self._symbol)
            score = self._minimax(new_board, False)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    
    def _minimax(self, board: Board, is_maximizing: bool):
        winner = board.check_winner()
        
        if winner == self._symbol:
            return 1
        elif winner == self._opponent:
            return -1
        elif winner == 'DRAW':
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for move in board.valid_moves():
                x, y = move
                new_board = board.simulate_move(x, y, self._symbol)
                score = self._minimax(new_board, False)
                best_score = max(score, best_score)
            
            return best_score
        else:
            best_score = float('inf')
            for move in board.valid_moves():
                x, y = move
                new_board = board.simulate_move(x, y, self._opponent)
                score = self._minimax(new_board, True)
                best_score = min(score, best_score)
            
            return best_score
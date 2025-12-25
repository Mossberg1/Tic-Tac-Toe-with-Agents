from agent import Agent
from board import Board

class MinimaxAgent(Agent):
    def __init__(self, symbol):
        self._symbol = symbol    
        self._opponent = 'O' if symbol == 'X' else 'X'
        self._cache = {}
    
    def select_action(self, board: Board) -> tuple[int, int]:
        #self._cache = {}
        
        best_score = float('-inf')
        best_move = None
        
        alpha = float('-inf')
        beta = float('inf')
        
        for move in board.valid_moves():
            x, y = move
            new_board = board.simulate_move(x, y, self._symbol)
            if new_board.check_winner() == self._symbol:
                return move
            
            score = self._minimax(new_board, False, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = move
                
            alpha = max(alpha, best_score)
        
        return best_move
    
    
    def _minimax(self, board: Board, is_maximizing: bool, alpha: float, beta: float):
        state_key = str(board)
        if state_key in self._cache:
            return self._cache[state_key]
        
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
                score = self._minimax(new_board, False, alpha, beta)
                best_score = max(score, best_score)
                
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            
            self._cache[state_key] = best_score
            
            return best_score
        else:
            best_score = float('inf')
            for move in board.valid_moves():
                x, y = move
                new_board = board.simulate_move(x, y, self._opponent)
                score = self._minimax(new_board, True, alpha, beta)
                best_score = min(score, best_score)
                
                beta = min(beta, score)
                if beta <= alpha:
                    break
            
            self._cache[state_key] = best_score
            
            return best_score
from agent import Agent

class MinimaxAgent(Agent):
    def __init__(self, symbol):
        self._symbol = symbol
        self._opponent = 'O' if symbol == 'X' else 'X'
    
    
    def select_action(self, board):
        best_score = -float('inf')
        best_action = None
        
        for move in self._get_valid_moves(board):
            new_board = self._apply_move(board, move, self._symbol)
            score = self._minimax(new_board, False)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move 
    
    
    def _minimax(self, state, is_max):
        pass

    def _get_valid_moves(board):
        raise NotImplementedError()
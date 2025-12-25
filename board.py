import copy
from utils import valid_symbol


class Board:
    def __init__(self):
        self._board = Board._generate_board()
        
    
    def check_winner(self) -> str:
        winner = None
        board_ref = self._board
        
        for row in range(0, 3):
            if((board_ref[row][0] == board_ref[row][1] == board_ref[row][2]) and (board_ref[row][0] is not None)):
                winner = board_ref[row][0]
                return winner
    
        for col in range(0, 3):
            if((board_ref[0][col] == board_ref[1][col] == board_ref[2][col]) and (board_ref[0][col] is not None)):
                winner =  board_ref[0][col]
                return winner
    
        if (board_ref[0][0] == board_ref[1][1] == board_ref[2][2]) and (board_ref[0][0] is not None):
            winner =  board_ref[0][0]
            return winner
            
        if (board_ref[0][2] == board_ref[1][1] == board_ref[2][0]) and (board_ref[0][2] is not None):
            winner =  board_ref[0][2]
            return winner
        
        if winner is None:
            for i in range(len(board_ref)):
                for j in range(len(board_ref)):
                    if board_ref[i][j] != 'X' and board_ref[i][j] != 'O':
                        return None
            return "DRAW"
    
    
    def clear_board(self):
        self._board = Board._generate_board()
    
    
    def is_free(self, x: int, y: int) -> bool:
        return self._board[y][x] != 'O' and self._board[y][x] != 'X'
    
    
    def make_move(self, x: int, y: int, symbol: str):
        if not valid_symbol(symbol):
            raise ValueError('Not a valid symbol')
        self._board[y][x] = symbol
    
    
    def simulate_move(self, x: int, y: int, symbol: str) -> 'Board':
        new_board = self._copy()
        new_board.make_move(x, y, symbol)
        return new_board
    
    
    def valid_moves(self) -> list[tuple[int, int]]:
        moves = list()
        for y in range(3):
            for x in range(3):
                if self.is_free(x, y):
                    moves.append((x, y))
        return moves

    
    def _copy(self) -> 'Board':
        new_board = Board()
        new_board._board = copy.deepcopy(self._board)
        return new_board
    
    
    @staticmethod
    def _generate_board() -> list[list[int]]:
        return [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
    
    
    def __str__(self):
        return ''.join(str(cell) if cell in ['X', 'O'] else '_' for row in self._board for cell in row)
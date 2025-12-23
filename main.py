import pygame
import sys
import time
from minimax_agent import MinimaxAgent
from mouse import get_mouse_pos
from board import Board
from utils import valid_symbol


pygame.init()


WIDTH, HEIGHT = 900, 900
FONT = pygame.font.Font('assets/Roboto-Regular.ttf', 100)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
BOARD = pygame.image.load('assets/Board.png')
X_IMG = pygame.image.load('assets/X.png')
O_IMG = pygame.image.load('assets/O.png')
BG_COLOR = (214, 201, 227)


board = Board()
graphical_board = [
    [[None, None], [None, None], [None, None]],
    [[None, None], [None, None], [None, None]],
    [[None, None], [None, None], [None, None]]
]


SCREEN.fill(BG_COLOR)
SCREEN.blit(BOARD, (64, 64))


pygame.display.update()


def make_move(symbol: str) -> bool:
    if not valid_symbol(symbol):
        raise ValueError('Not a valid symbol')
    
    x, y = get_mouse_pos()
    
    if board.is_free(x, y):
        board.make_move(x, y, symbol)
        return True
    
    return False


def render_board():
    board_ref = board._board
    
    for i in range(3):
        for j in range(3):
            if board_ref[i][j] == 'X':
                graphical_board[i][j][0] = X_IMG
                graphical_board[i][j][1] = X_IMG.get_rect(center=(j*300+150, i*300+150))
            elif board_ref[i][j] == 'O':
                graphical_board[i][j][0] = O_IMG
                graphical_board[i][j][1] = O_IMG.get_rect(center=(j*300+150, i*300+150))
            
            if graphical_board[i][j][0] is not None:
                SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])
          
             
symbol = 'X'
        
                
def clear_board():
    board.clear_board()
    graphical_board = [
        [[None, None], [None, None], [None, None]],
        [[None, None], [None, None], [None, None]],
        [[None, None], [None, None], [None, None]]
    ]
    
    symbol = 'X'
    
    SCREEN.fill(BG_COLOR)
    SCREEN.blit(BOARD, (64, 64))


agent_symbol = 'O'
agent = MinimaxAgent(agent_symbol)

human_symbol = 'X'


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Human move
        if event.type == pygame.MOUSEBUTTONDOWN and symbol == human_symbol:
            if make_move(symbol):
                symbol = agent_symbol
    
    if symbol == agent_symbol:
        move = agent.select_action(board)
        if move:
            x, y = move
            board.make_move(x, y, agent_symbol)
            symbol = human_symbol
    
    render_board()
    pygame.display.update()
    
    winner = board.check_winner()
    
    if winner is not None:
        print(winner)
        time.sleep(2)
        clear_board()
        sys.exit()
        
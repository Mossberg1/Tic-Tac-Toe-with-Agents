import pygame
import sys
import time
import os
import pickle
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from qlearn_agent import QLearnAgent
from random_agent import RandomAgent
from minimax_agent import MinimaxAgent
from reference_agent import ReferenceAgent
from mouse import get_mouse_pos
from board import Board
from utils import valid_symbol
from qlearn import train 


parser = argparse.ArgumentParser(description='Tic Tac Toe RL Agent')
parser.add_argument('-d', '--delete', action='store_true', help='Delete all saved .pkl models before starting')
parser.add_argument('-p', '--plot', action='store_true', help='Plot the learning curve of the model')
args = parser.parse_args()


if args.delete:
    pkl_files = glob('*.pkl')
    if pkl_files: 
        for file in pkl_files:
            try:
                os.remove(file)
                print(f' - Deleted: {file}')
            except OSError as ex:
                print(f' - Error deleting {file}: {ex}')
    else:
        print('No saved models found')


MODEL_FILE = 'model.pkl'
POLICY_FILE = 'perfectPolicy.p'

use_reference_agent = False
use_minimax_agent = False

agent = QLearnAgent(symbol='O', learning_rate=0.1, discount_factor=0.9, exploration_rate=0.5)

if os.path.exists(MODEL_FILE):
    print('Loading saved model...')
    
    agent.load_model(MODEL_FILE)
    agent._exploration_rate = 0
else: 
    print("No saved model found. Starting training against Reference Policy...")

    if use_reference_agent:    
        with open(POLICY_FILE, 'rb') as f:
            reference_model_data = pickle.load(f)
        training_opponent = ReferenceAgent(symbol='X', model_data=reference_model_data)
        print("Training against Imported Reference Model...")
    elif use_minimax_agent:
        training_opponent = MinimaxAgent(symbol='X')
        print('Training against MinimaxAgent')
    else:
        training_opponent = RandomAgent(symbol='X')
        print('Training against RandomAgent')
        
    results = train(agent, training_opponent, epochs=100000)
    
    agent.save_model(MODEL_FILE)

    if args.plot: # Plot learning curve if -p cli argument is present
        df = pd.DataFrame(results, columns=['result'])
        
        window_size = 1000
        df['win_rate'] = df['result'].apply(lambda x: 1 if x == 1 else 0).rolling(window=window_size).mean()
        df['loss_rate'] = df['result'].apply(lambda x: 1 if x == -1 else 0).rolling(window=window_size).mean()
        df['draw_rate'] = df['result'].apply(lambda x: 1 if x == 0 else 0).rolling(window=window_size).mean()

        plt.figure(figsize=(12, 6))
        plt.plot(df['win_rate'], label='Win Rate', color='green')
        plt.plot(df['draw_rate'], label='Draw Rate', color='blue', linestyle='--')
        plt.plot(df['loss_rate'], label='Loss Rate', color='red', linestyle='--')
        
        plt.title('Agent Learning Curve (vs Reference Policy Only)')
        plt.xlabel('Games Played')
        plt.ylabel('Rate')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

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
human_symbol = 'X'


# Game loop
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
        

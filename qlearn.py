from board import Board
from agent import Agent
from tqdm import tqdm
from qlearn_agent import QLearnAgent
from minimax_agent import MinimaxAgent

BASE_REWARD = 0
DRAW_REWARD = 5
LOSS_PENALTY = -10
WIN_REWARD = 10



def train(agent: QLearnAgent, opponent: Agent, epochs: int):
    history = []
    
    for epoch in tqdm(range(epochs), desc="Training"):
        board = Board()
        current_symbol = 'X'
        
        last_state = None
        last_action = None
        
        while board.check_winner() is None:
            if current_symbol == agent._symbol:
                if last_state is not None:
                    agent.learn(last_state, last_action, BASE_REWARD, board)
                
                
                state_before = board._copy()
                action = agent.select_action(board)
                if action is None:
                    break
                
                x, y = action
                board.make_move(x, y, agent._symbol)
                
                last_state = state_before
                last_action = action 
                
                winner = board.check_winner()
                
                if winner == agent._symbol: 
                    agent.learn(last_state, last_action, WIN_REWARD, board)
                    history.append(1) # Win
                elif winner == 'DRAW': 
                    agent.learn(last_state, last_action, DRAW_REWARD, board)
                    history.append(0) # Draw
                
                current_symbol = 'X'
            else:
                action = opponent.select_action(board)
                x, y = action 
                board.make_move(x, y, 'X')
                
                winner = board.check_winner()
                
                if winner == 'X':
                    if last_state:
                        agent.learn(last_state, last_action, LOSS_PENALTY, board)
                    history.append(-1) # Loss
                elif winner == 'DRAW':
                    if last_state:
                        agent.learn(last_state, last_action, DRAW_REWARD, board)
                    history.append(0) # Draw
                
                current_symbol = agent._symbol
                
        agent._exploration_rate *= 0.99995
        
    agent._exploration_rate = 0
    
    return history

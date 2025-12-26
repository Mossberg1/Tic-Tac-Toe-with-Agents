from board import Board
from agent import Agent
from tqdm import tqdm
from qlearn_agent import QLearnAgent
from minimax_agent import MinimaxAgent


def train(agent: QLearnAgent, opponent: Agent, epochs: int):
    history = []
    
    for epoch in tqdm(range(epochs), desc="Training"):
        board = Board()
        current_symbol = 'X'
        
        last_state = None
        last_action = None
        
        while board.check_winner() is None:
            if current_symbol == agent._symbol:
                state_before = board._copy()
                action = agent.select_action(board)
                x, y = action
                board.make_move(x, y, agent._symbol)
                
                last_state = state_before
                last_action = action 
                
                reward = 0
                
                winner = board.check_winner()
                
                if winner == agent._symbol: 
                    reward = 10
                    history.append(1) # Win
                elif winner == 'DRAW': 
                    reward = 5
                    history.append(0) # Draw
                
                agent.learn(state_before, action, reward, board)
                current_symbol = 'X'
            else:
                action = opponent.select_action(board)
                x, y = action 
                board.make_move(x, y, 'X')
                
                winner = board.check_winner()
                
                if winner == 'X':
                    if last_state:
                        agent.learn(last_state, last_action, -100, board)
                    history.append(-1) # Loss
                elif winner == 'DRAW':
                    if last_state:
                        agent.learn(last_state, last_action, 5, board)
                    history.append(0) # Draw
                
                current_symbol = 'O'
                
        agent._exploration_rate *= 0.99995
        
    agent._exploration_rate = 0
    
    return history
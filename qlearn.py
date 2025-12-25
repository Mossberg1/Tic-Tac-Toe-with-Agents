from board import Board
from agent import Agent
from qlearn_agent import QLearnAgent
from minimax_agent import MinimaxAgent


def train(agent: QLearnAgent, opponent: Agent, epochs: int):
    for epoch in range(epochs):
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
                
                if winner == agent._symbol: reward = 1
                elif winner == 'DRAW': reward = 0.5
                
                agent.learn(state_before, action, reward, board)
                current_symbol = 'X'
            else:
                action = opponent.select_action(board)
                x, y = action 
                board.make_move(x, y, 'X')
                
                if board.check_winner() == 'X':
                    if last_state:
                        agent.learn(last_state, last_action, -1, board)
                
                current_symbol = 'O'
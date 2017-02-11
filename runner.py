from simulator import Simulator

if __name__ == "__main__":
    '''
    Runner code to start the training and game play.
    '''
    alpha_value = 0
    gamma_value = 0
    epsilon_value = 0
    num_games = 0
    sim = Simulator(num_games, alpha_value, gamma_value, epsilon_value)
    sim.train_agent()


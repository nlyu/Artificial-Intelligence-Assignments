import MDP
from graphics import *
import random

class Simulator:
    '''
        Q Table is a map that maps a set of state+actions to a value (ball_x, ball_y, vx, vy, py, paddle_movement) -> Utility
    '''
    def __init__(self, num_games=0, alpha_value=0, gamma_value=0, epsilon_value=0):
        '''
        Setup the Simulator with the provided values.
        :param num_games - number of games to be trained on.
        :param alpha_value - 1/alpha_value is the decay constant.
        :param gamma_value - Discount Factor.
        :param epsilon_value - Probability value for the epsilon-greedy approach.
        '''
        self.num_games = num_games
        self.epsilon_value = epsilon_value
        self.alpha_value = alpha_value
        self.gamma_val = gamma_value

        self.QTable = {}

        #GUI
        """
        self.win = GraphWin("Pong Game", 700, 700)
        self.ball = Circle(Point(350,350), 20)
        msg = Text(Point(330, 25), "Pong Game")
        msg.draw(self.win)
        for i in range(0, 12):
            for j in range(0, 12):
                c = Rectangle(Point(50 + i*50, 50 + j*50), Point(100 + i*50, 100 + j*50))
                c.draw(self.win)
        self.p = Rectangle(Point(600, 250), Point(650, 400))
        self.p.setFill("red")
        self.p.draw(self.win)
        self.ball.draw(self.win)
        """


        # Init the Q Table to be all zeros
        for ball_x in range(12):
            for ball_y in range(12):
                for vx in [-1, 1]:
                    for vy in [-1, 0, 1]:
                        for py in range(12):
                            for action in range(3):
                                key = tuple([ball_x, ball_y, vx, vy, py, action])
                                self.QTable[key] = 0

        self.QTable[-1] = 0
        self.action_strs = ["NOTHING", "UP", "DOWN"]
        self.best_score = 0

    def f_function(self, state_tuple):
        '''
        Choose action based on an epsilon greedy approach
        At first, let's ignore the epsilon greedy approach
        We'll just pick any one of the three paddle movement, which produces the largest utility
        '''
        a = random.random();
        action_selected = random.randint(0, 2)

        do_nothing = state_tuple + (0,)
        do_up = state_tuple + (1,)
        do_down = state_tuple + (2,)

        utility_p_nothing = self.QTable[do_nothing]
        utility_p_up = self.QTable[do_up]
        utility_p_down = self.QTable[do_down]
        if (a >= self.epsilon_value):
            if utility_p_nothing > utility_p_up and utility_p_nothing > utility_p_down:
                action_selected = 0
            if utility_p_up > utility_p_down and utility_p_up > utility_p_nothing:
                action_selected = 1
            if utility_p_down > utility_p_up and utility_p_down > utility_p_nothing:
                action_selected = 2
        else:
            action_selected = random.randint(0, 2)

        return action_selected

    def train_agent(self):
        '''
        Train the agent over a certain number of games.
        '''
        n = self.num_games
        while n != 0:
            self.play_game()
            n = n - 1
            print n, " rounds remaining..."
        #self.win.close()
        print "Best score of all time: ", self.best_score
        pass


    def play_game(self):
        '''
        Simulate an actual game till the agent loses.
        
        '''
        # Create a MDP to track state transitions
        mdp = MDP.MDP()

        curr_state = mdp.discretize_state()
        last_state = mdp.discretize_state()
        last_action = 1
        # self.draw_gui(curr_state, last_state)
        reward = 0
        special_state_key = -1
        # Call simulate_one_time_step in a loop, until game fails(ball pass the paddle)
        counter = 0
        while 1:
            # Select action and simulate time step
            action_selected = self.f_function(curr_state)
            # print "Action selected is " + self.action_strs[action_selected]
            mdp.simulate_one_time_step(action_selected)
            curr_state = mdp.discretize_state()
            #if curr_state[0] != last_state[0] or curr_state[1] != last_state[1]:
            #    self.draw_gui(curr_state, last_state)
            # print "the current positioin: ", curr_state[0], curr_state[1]
            # Update Q Table
            reward = mdp.read_curr_reward()
            if reward == 1:
                counter = counter + 1
                if counter > self.best_score:
                    self.best_score = counter
                    print "best", self.best_score

            if mdp.is_in_special_state():
                err = self.alpha_value * (reward + self.QTable[-1] - self.QTable[last_state + (last_action,)])
                self.QTable[last_state + (last_action,)] = self.QTable[last_state + (last_action,)] + err
                # print "errrrrrrrrenddddddddd"
            else:
                err = self.alpha_value * (reward + self.QTable[curr_state + (action_selected,)] - self.QTable[last_state + (last_action,)])
                self.QTable[last_state + (last_action,)] = self.QTable[last_state + (last_action,)] + err

            if mdp.is_in_special_state():
                break

            last_state = curr_state
            last_action = action_selected
        pass

    def draw_gui(self, cur, pre):
        x = cur[0] - pre[0]
        y = cur[1] - pre[1]

        # Draw ball
        self.ball.undraw()
        self.ball = Circle(Point(50+50*cur[0]+25, 50+50*cur[1]+25), 20)
        self.ball.draw(self.win)
        self.p.undraw()

        # Draw paddle
        self.p = Rectangle(Point(600, 50 * cur[4]), Point(650, 50 * cur[4] + 120))
        self.p.setFill("red")
        self.p.draw(self.win)
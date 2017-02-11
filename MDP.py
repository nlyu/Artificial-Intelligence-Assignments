import random
import math

class MDP:

    def __init__(self,
                 ball_x=None,
                 ball_y=None,
                 velocity_x=None,
                 velocity_y=None,
                 paddle_y=None):
        '''
        Setup MDP with the initial values provided.
        '''
        self.create_state(
            ball_x=ball_x,
            ball_y=ball_y,
            velocity_x=velocity_x,
            velocity_y=velocity_y,
            paddle_y=paddle_y
        )

        # the agent can choose between 3 actions - stay, up or down respectively.
        self.actions = [0, 0.04, -0.04]
        self.reward = 0

    def create_state(self,
              ball_x=None,
              ball_y=None,
              velocity_x=None,
              velocity_y=None,
              paddle_y=None):
        '''
        Helper function for the initializer. Initialize member variables with provided or default values.
        '''
        self.paddle_height = 0.2
        self.ball_x = ball_x if ball_x != None else 0.5
        self.ball_y = ball_y if ball_y != None else 0.5
        self.velocity_x = velocity_x if velocity_x != None else 0.03
        self.velocity_y = velocity_y if velocity_y != None else 0.01
        self.paddle_x = 1
        self.paddle_y = 0.5

    def simulate_one_time_step(self, action_selected):
        '''
        :param action_selected - Current action to execute.
        Perform the action on the current continuous state.
        '''
        # Your Code Goes Here!

        # First update ball position, since this function simulates exactly one time step, all we should do is add velocity to current ball positions
        self.ball_x = self.ball_x + self.velocity_x
        self.ball_y = self.ball_y + self.velocity_y

        # Second, update paddle positions according to action_selected(0, -0.04, 0.04), also check that paddle cannot move off the screen
        self.paddle_y = self.paddle_y + self.actions[action_selected]
        if self.paddle_y < 0:
            self.paddle_y = 0
        if self.paddle_y > 1 - self.paddle_height:
            self.paddle_y = 1 - self.paddle_height

        # Third, collision detection (Wall and paddle)
        if self.ball_y < 0:
            self.ball_y = -self.ball_y
            self.velocity_y = -self.velocity_y

        if self.ball_y > 1:
            self.ball_y = 2 - self.ball_y
            self.velocity_y = -self.velocity_y

        if self.ball_x < 0:
            self.ball_x = -self.ball_x
            self.velocity_x = self.velocity_x

        if self.ball_x == self.paddle_x and (self.ball_y >= self.paddle_y and self.ball_y <= self.paddle_y + self.paddle_height):
            self.ball_x = 2 * self.paddle_x - self.ball_x
            self.velocity_x = -self.velocity_x + random.uniform(-0.015, 0.015)
            self.velocity_y = self.velocity_y + random.uniform(-0.03, 0.03)
            if math.fabs(self.velocity_x <= 0.03):
                self.velocity_x = 0.04 if self.velocity_x > 0 else -0.04
            self.reward = 1
            print "hit the panel!"

        if self.ball_x > 1:
            self.reward = -1
            print "out of bone!"

        # Restrict velocity to be below 1
        if math.fabs(self.velocity_x > 1):
            self.velocity_x = 1 if self.velocity_x > 0 else -1
        if math.fabs(self.velocity_y > 1):
            self.velocity_y = 1 if self.velocity_y > 0 else -1
        pass

    def discretize_state(self):
        '''
        Convert the current continuous state to a discrete state.
        '''

        # Convert ball_x to discrete

        t = math.floor(12 * self.ball_x)
        if t <= 12 and t >= 11:
            dball_x = 11
        else:
            dball_x = int(t)

        # Convert ball_y to discrete
        t = math.floor(12 * self.ball_y)
        if t <= 12 and t >= 11:
            dball_y = 11
        else:
            dball_y = int(t)

        # Convert vx to discrete
        dvelocity_x = 1 if self.velocity_x > 0 else -1

        # Convert vy to discrete
        if math.fabs(self.velocity_y) <= 0.015:
            dvelocity_y = 0
        elif dvelocity_y > 0:
            dvelocity_y = 1
        elif dvelocity_y < 0:
            dvelocity_y = -1
        
        # Convert paddle_y to discrete
        dpaddle_y = math.floor(12 * self.paddle_y / (1 - self.paddle_height))
        if self.paddle_y == 1 - self.paddle_height:
            dpaddle_y = 11
        return tuple([dball_x, dball_y, dvelocity_x, dvelocity_y, dpaddle_y])

    def is_in_special_state(self):
        curr_state = self.discretize_state();
        if curr_state[0] > 11:
            return True
        return False

    def read_curr_reward(self):
        t = self.reward
        self.reward = 0
        return t
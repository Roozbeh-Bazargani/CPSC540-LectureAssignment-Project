import pygame
import numpy as np
import random

GRID_SIZE = 10

grid = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

class Player:
    def __init__(self, movements_txt, goal):
        self.x = 0
        self.y = GRID_SIZE - 1
        self.goal_x = goal[0] #GRID_SIZE - 1
        self.goal_y = goal[1] #0
        self.path = []
        self.movements = movements_txt.split(", ")

    def movement_in_board(self):
        if (self.x < 0) or (self.x >= GRID_SIZE):
            return False
        if (self.y < 0) or (self.y >= GRID_SIZE):
            return False
        return True

    def movement_allowed(self):
        if grid[self.y][self.x] == 1:
            return False
        return True

    def goal_reached(self):
        if (self.y == self.goal_y) and (self.x == self.goal_x):
            return True
        return False

    def find_player_path(self):
        path_allowed = True
        self.path.append((self.y, self.x))

        for move in self.movements:
            if move == 'R':
                self.x = self.x + 1
            if move == 'L':
                self.x = self.x - 1
            if move == 'U':
                self.y = self.y - 1
            if move == 'D':
                self.y = self.y + 1
            if move == 'UR':
                self.y = self.y - 1
                self.x = self.x + 1
            if move == 'DR':
                self.y = self.y + 1
                self.x = self.x + 1
            if move == 'UL':
                self.y = self.y - 1
                self.x = self.x - 1
            if move == 'DL':
                self.y = self.y + 1
                self.x = self.x - 1

            if not self.movement_allowed():
                path_allowed = False

            if not self.movement_in_board():
                return None
            else:
                self.path.append((self.y, self.x))

        return self.path, path_allowed, self.goal_reached()

class App:
    black = (0, 0, 0)
    white = (255, 255, 255)
    blue = (50, 127, 168)
    red = (255, 0, 0)
    green = (0,255,0)
    orange = (255,215,0)

    WIDTH = 20
    HEIGHT = 20
    MARGIN = 5

    window_size = [255, 255]

    def __init__(self, movements_txt, goal):
        self._running = True
        self.player_movements_txt = movements_txt
        self.goal = goal

    def on_init(self):
        pygame.init()
        self.scr = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Assignment Game")

    def check_event(self):
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                self._running = False

    def on_cleanup(self):
        pygame.quit()

    def on_render(self):
        player_path, player_path_allowed, player_goal_reached = Player(self.player_movements_txt, self.goal).find_player_path()
        if player_path is None:
            print("The set of movements is not allowed. (you've moved outside of the board range)")
            self.done=True
        # if not player_path_allowed:
        #     print("The set of movements is not allowed. (you've moved in the blocked cells")
        # if not player_goal_reached:
        #     print("Your agent didn't reach the goal.")

        self.scr.fill(self.black)
        for row in range(GRID_SIZE):
            for column in range(GRID_SIZE):
                color = self.white
                if (row, column) in player_path:
                    if grid[row][column] == 1:
                        color = self.red
                    elif player_path.index((row, column)) == (len(player_path)-1):
                        if player_goal_reached:
                            color = self.green
                        else:
                            color = self.orange
                    else:
                        color = self.blue
                elif grid[row][column] == 1:
                    color = self.black
                pygame.draw.rect(self.scr,
                                 color,
                                 [(self.MARGIN + self.WIDTH) * column + self.MARGIN,
                                  (self.MARGIN + self.HEIGHT) * row + self.MARGIN,
                                  self.WIDTH,
                                  self.HEIGHT])
        pygame.display.flip()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            self.check_event()
            self.on_render()
        self.on_cleanup()

# Students Should complete this code for the assignment
class Agent(object):
    def __init__(self, grid, goal):
        self.grid = grid
        self.start = np.array([0, GRID_SIZE - 1])
        self.goal = np.array(goal)
    def solve(self):
        action_list = ['R', 'L', 'U', 'D', 'UR', 'DR', 'UL', 'DL']#, 'S']
        actions = {'R': np.array([1, 0]), 'L': np.array([-1, 0]), 'U': np.array([0, -1]), 'D': np.array([0, 1]),
                   'UR': np.array([1, -1]), 'DR': np.array([1, 1]), 'UL': np.array([-1, -1]), 'DL': np.array([-1, 1])}#, 'S': np.array([0,0])}
        alpha = 0.9
        gama = 0.9
        max_iter = 50
        ## Solve here ##
        # Q = {'R': np.zeros((GRID_SIZE, GRID_SIZE)), 'L': np.zeros((GRID_SIZE, GRID_SIZE)), 'U': np.zeros((GRID_SIZE, GRID_SIZE)), 'D': np.zeros((GRID_SIZE, GRID_SIZE)),
        #      'UR': np.zeros((GRID_SIZE, GRID_SIZE)), 'DR': np.zeros((GRID_SIZE, GRID_SIZE)), 'UL': np.zeros((GRID_SIZE, GRID_SIZE)), 'DL': np.zeros((GRID_SIZE, GRID_SIZE))}
        Q = np.ones((len(action_list), GRID_SIZE, GRID_SIZE)) * (-20)
        V = np.ones((GRID_SIZE, GRID_SIZE)) * (-20)
        Policy = [[None for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
        for iter in range(max_iter):
            delta = 0
            for x in range(GRID_SIZE):
                for y in range(GRID_SIZE):
                    state = np.array([x, y])
                    V_old = V[x,y]
                    for i in range(len(action_list)):
                        a = action_list[i]
                        action = actions[a]
                        state_n = state + action # next state
                        if (state_n > 9).any() or (state_n < 0).any():
                            continue
                        R = -np.linalg.norm(action)
                        if grid[state_n[1]][state_n[0]]:
                            R = -1000
                        elif (state_n == self.goal).all():
                            R = 10
                        # updating
                        Q[i,x, y] = (1 - alpha)*Q[i,x, y] + alpha*(R + gama*np.max(Q[:,state_n[0], state_n[1]]))
                    V[x,y] = np.max(Q[:,x, y])
                    # print('hii', Q[:,x, y])
                    Policy[x][y] = action_list[np.argmax(Q[:,x, y])]
                    delta = np.maximum(delta, np.abs(V[x,y] - V_old))

        state = self.start
        path = ''
        # print(Q[0])
        # print(V)
        # print(Policy)
        while (state != self.goal).any():
            # print(state[0], state[1])
            a = Policy[state[0]][state[1]]
            path += a + ', '
            action = actions[a]
            state += action
        return path[:-2]



        ## END ##
        
if __name__ == "__main__" :
    goal = [GRID_SIZE - 1, 0]
    # player_movements_txt = 'R, U, U, U, U, U, U, U, U, U, R, R, R, DR, R, R, R, UR'
    player_movements_txt = Agent(grid, goal).solve()
    print(player_movements_txt)
    theApp = App(player_movements_txt, goal)
    theApp.on_execute()


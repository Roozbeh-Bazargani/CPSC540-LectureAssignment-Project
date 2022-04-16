import pygame

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
    def __init__(self, movements_txt):
        self.x = 0
        self.y = GRID_SIZE - 1
        self.path = []
        self.movements = movements_txt.split(", ")

    def movement_allowed(self):
        if (self.x < 0) or (self.x >= GRID_SIZE):
            return False
        if (self.y < 0) or (self.y >= GRID_SIZE):
            return False
        if grid[self.y][self.x] == 1:
            return False
        return True

    def find_player_path(self):
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

            if not self.movement_allowed():
                return None
            else:
                self.path.append((self.y, self.x))
        return self.path

class App:
    black = (0, 0, 0)
    white = (255, 255, 255)
    blue = (50, 127, 168)

    WIDTH = 20
    HEIGHT = 20
    MARGIN = 5

    window_size = [255, 255]

    def __init__(self, movements_txt):
        self._running = True
        # self._display_surf = None
        # self._image_surf = None
        self.player_movements_txt = movements_txt

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
        player_path = Player(self.player_movements_txt).find_player_path()
        if player_path is None:
            print("The set of movements is not allowed.")
            self.done=True
            # self.on_cleanup()

        self.scr.fill(self.black)
        for row in range(GRID_SIZE):
            for column in range(GRID_SIZE):
                color = self.white
                if (row, column) in player_path:
                    color = self.blue
                if grid[row][column] == 1:
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
    def __init__(self, grid):
        self.grid = grid
    def solve():
        pass
        
if __name__ == "__main__" :
    player_movements_txt = 'R, U, U, U, U, U, U, U, U, U, R, R, R, R, R, R, R, R'
    # player_movements_txt = Agent(grid).solve()
    theApp = App(player_movements_txt)
    theApp.on_execute()


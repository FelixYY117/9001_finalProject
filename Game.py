import pygame


import time
import sys
from Maze import Maze
from Player import Player

# Initialize Pygame
pygame.init()

# game constants
CELL_SIZE = 30
MAZE_WIDTH = 21  # must be odd
MAZE_HEIGHT = 21  # must be odd
WINDOW_WIDTH = MAZE_WIDTH * CELL_SIZE
WINDOW_HEIGHT = MAZE_HEIGHT * CELL_SIZE + 60  # Extra space to display information

# Color definition
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)


class Game:


    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Maze Game")
        self.clock = pygame.time.Clock()


        self.font = pygame.font.Font(None, 20)

        self.maze = Maze(MAZE_WIDTH, MAZE_HEIGHT)
        self.player = Player(1, 1)
        self.show_solution = False
        self.game_completed = False
        self.start_time = time.time()

        # generate maze
        self.maze.generate_maze()
        self.maze.find_shortest_path()

    def draw(self):
        """ Draw the game screen """
        self.screen.fill(WHITE)

        # plot the maze
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE,
                                   CELL_SIZE, CELL_SIZE)

                if self.maze.grid[y][x] == 1:
                    # walls
                    pygame.draw.rect(self.screen, BLACK, rect)
                else:
                    # Access
                    pygame.draw.rect(self.screen, WHITE, rect)
                    pygame.draw.rect(self.screen, GRAY, rect, 1)

        # Plot the start and end points
        start_rect = pygame.Rect(self.maze.start[0] * CELL_SIZE,
                                 self.maze.start[1] * CELL_SIZE,
                                 CELL_SIZE, CELL_SIZE)
        end_rect = pygame.Rect(self.maze.end[0] * CELL_SIZE,
                               self.maze.end[1] * CELL_SIZE,
                               CELL_SIZE, CELL_SIZE)

        pygame.draw.rect(self.screen, GREEN, start_rect)
        pygame.draw.rect(self.screen, RED, end_rect)

        # plot the solution path
        if self.show_solution and self.maze.solution_path:
            for i in range(len(self.maze.solution_path) - 1):
                x1, y1 = self.maze.solution_path[i]
                x2, y2 = self.maze.solution_path[i + 1]

                pos1 = (x1 * CELL_SIZE + CELL_SIZE // 2,
                        y1 * CELL_SIZE + CELL_SIZE // 2)
                pos2 = (x2 * CELL_SIZE + CELL_SIZE // 2,
                        y2 * CELL_SIZE + CELL_SIZE // 2)

                pygame.draw.line(self.screen, LIGHT_BLUE, pos1, pos2, 3)

        # Draw players
        player_rect = pygame.Rect(self.player.x * CELL_SIZE + 5,
                                  self.player.y * CELL_SIZE + 5,
                                  CELL_SIZE - 10, CELL_SIZE - 10)
        pygame.draw.ellipse(self.screen, BLUE, player_rect)

        #  plot game info
        elapsed_time = int(time.time() - self.start_time)
        info_y = MAZE_HEIGHT * CELL_SIZE + 5

        # Time
        time_text = self.font.render(f"Time: {elapsed_time}s", True, BLACK)
        self.screen.blit(time_text, (10, info_y))

        # Move
        moves_text = self.font.render(f"Moves: {self.player.moves}", True, BLACK)
        self.screen.blit(moves_text, (150, info_y))

        # Tip
        hint_text = self.font.render("H:Show/Hide Path  R:Reset", True, BLACK)
        self.screen.blit(hint_text, (10, info_y + 25))

        # If the game is complete
        if self.game_completed:
            win_text = self.font.render("Congratulations! Press R to restart", True, RED)
            text_rect = win_text.get_rect(center=(WINDOW_WIDTH // 2,
                                                  WINDOW_HEIGHT - 10))
            self.screen.blit(win_text, text_rect)

        pygame.display.flip()

    def reset_game(self):
        """ Reset game """
        self.maze = Maze(MAZE_WIDTH, MAZE_HEIGHT)
        self.maze.generate_maze()
        self.maze.find_shortest_path()

        self.player = Player(1, 1)
        self.show_solution = False
        self.game_completed = False
        self.start_time = time.time()

    def handle_keydown(self, event):
        """ Handling key events """
        if not self.game_completed:
            # Player move
            if event.key == pygame.K_UP:
                self.player.move(0, -1, self.maze)
            elif event.key == pygame.K_DOWN:
                self.player.move(0, 1, self.maze)
            elif event.key == pygame.K_LEFT:
                self.player.move(-1, 0, self.maze)
            elif event.key == pygame.K_RIGHT:
                self.player.move(1, 0, self.maze)

            # Check if you've reached the finish line
            if (self.player.x, self.player.y) == self.maze.end:
                self.game_completed = True

        # Show/hide the solution
        if event.key == pygame.K_h:
            self.show_solution = not self.show_solution

        # Restart
        if event.key == pygame.K_r:
            self.reset_game()

    def run(self):
        """ Main game loop """
        running = True

        while running:
            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)

            # plot the screen
            self.draw()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
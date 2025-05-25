import random
from collections import deque

class Maze:
    """ Maze class, responsible for generating and managing mazes. """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[1 for _ in range(width)] for _ in range(height)]
        self.start = (1, 1)
        self.end = (width - 2, height - 2)
        self.solution_path = []

    def generate_maze(self):
        """ Using recursive backtracking to generate a maze """
        # Initialize maze, all walls (1)
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]

        # create access tags
        visited = [[False for _ in range(self.width)] for _ in range(self.height)]

        # Recursively generate the maze
        self._carve_path(1, 1, visited)

        # Make sure the start and end points are paths
        self.grid[self.start[1]][self.start[0]] = 0
        self.grid[self.end[1]][self.end[0]] = 0

    def _carve_path(self, x, y, visited):
        """ Recursively dig through the path """
        # Mark the current location as visited
        visited[y][x] = True
        self.grid[y][x] = 0  # Let be a path

        # List of random directions
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check if the new location is valid and not visited
            if (1 <= nx < self.width - 1 and
                    1 <= ny < self.height - 1 and
                    not visited[ny][nx]):
                # Break through the wall
                wall_x = x + dx // 2
                wall_y = y + dy // 2
                self.grid[wall_y][wall_x] = 0

                # Recursively visit the new location
                self._carve_path(nx, ny, visited)

    def find_shortest_path(self):
        """ Find the shortest path """

        self.solution_path = []


        queue = deque([(self.start[0], self.start[1], [])])
        visited = set()
        visited.add(self.start)

        while queue:
            x, y, path = queue.popleft()
            current_path = path + [(x, y)]

            # Reach the end
            if (x, y) == self.end:
                self.solution_path = current_path
                return True

            # Check four directions
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy

                if (0 <= nx < self.width and
                        0 <= ny < self.height and
                        self.grid[ny][nx] == 0 and
                        (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append((nx, ny, current_path))

        return False
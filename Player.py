class Player:
    """玩家类"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.moves = 0

    def move(self, dx, dy, maze):
        """移动玩家"""
        new_x = self.x + dx
        new_y = self.y + dy

        # 检查是否可以移动
        if (0 <= new_x < maze.width and
                0 <= new_y < maze.height and
                maze.grid[new_y][new_x] == 0):
            self.x = new_x
            self.y = new_y
            self.moves += 1
            return True
        return False
import curses
import random
import pygad
import numpy as np

class Board():
    def __init__(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.emptyTiles = [(i, j) for i in range(4) for j in range(4)]
        self.nEmptyTiles = 16
        self.spawnTile()
        self.gameOver = False
        self.maxTile = 0
    
    def reset(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.emptyTiles = [(i, j) for i in range(4) for j in range(4)]
        self.nEmptyTiles = 16
        self.spawnTile()
        self.gameOver = False
    
    def getMaxTile(self):
        return self.maxTile

    def getGrid(self):
        return self.grid

    def getScore(self):
        return self.score

    def getEmptyTiles(self):
        return self.emptyTiles

    def moveLeft(self):
        changed = False
        for i in range(4):
            oldRow = self.grid[i][:]
            newRow = [x for x in self.grid[i] if x != 0]
            mergedRow = []
            skip = False
            for j in range(len(newRow)):
                if skip:
                    skip = False
                    continue
                if j < len(newRow) - 1 and newRow[j] == newRow[j + 1]:
                    mergedRow.append(newRow[j] * 2)
                    self.score += newRow[j] * 2
                    skip = True
                else:
                    mergedRow.append(newRow[j])
            mergedRow += [0] * (4 - len(mergedRow))
            if mergedRow != oldRow:
                changed = True
            self.grid[i] = mergedRow
        return changed

    def moveRight(self):
        changed = False
        for i in range(4):
            oldRow = self.grid[i][:]
            newRow = [x for x in self.grid[i] if x != 0]
            mergedRow = []
            skip = False
            for j in range(len(newRow) - 1, -1, -1):
                if skip:
                    skip = False
                    continue
                if j > 0 and newRow[j] == newRow[j - 1]:
                    mergedRow.append(newRow[j] * 2)
                    self.score += newRow[j] * 2
                    skip = True
                else:
                    mergedRow.append(newRow[j])
            mergedRow += [0] * (4 - len(mergedRow))
            mergedRow = mergedRow[::-1]
            if mergedRow != oldRow:
                changed = True
            self.grid[i] = mergedRow
        return changed

    def moveUp(self):
        changed = False
        for j in range(4):
            oldCol = [self.grid[i][j] for i in range(4)]
            newCol = [self.grid[i][j] for i in range(4) if self.grid[i][j] != 0]
            mergedCol = []
            skip = False
            for i in range(len(newCol)):
                if skip:
                    skip = False
                    continue
                if i < len(newCol) - 1 and newCol[i] == newCol[i + 1]:
                    mergedCol.append(newCol[i] * 2)
                    self.score += newCol[i] * 2
                    skip = True
                else:
                    mergedCol.append(newCol[i])
            mergedCol += [0] * (4 - len(mergedCol))
            if mergedCol != oldCol:
                changed = True
            for i in range(4):
                self.grid[i][j] = mergedCol[i]
        return changed

    def moveDown(self):
        changed = False
        for j in range(4):
            oldCol = [self.grid[i][j] for i in range(4)]
            newCol = [self.grid[i][j] for i in range(4) if self.grid[i][j] != 0]
            mergedCol = []
            skip = False
            for i in range(len(newCol) - 1, -1, -1):
                if skip:
                    skip = False
                    continue
                if i > 0 and newCol[i] == newCol[i - 1]:
                    mergedCol.append(newCol[i] * 2)
                    self.score += newCol[i] * 2
                    skip = True
                else:
                    mergedCol.append(newCol[i])
            mergedCol += [0] * (4 - len(mergedCol))
            mergedCol = mergedCol[::-1]
            if mergedCol != oldCol:
                changed = True
            for i in range(4):
                self.grid[i][j] = mergedCol[i]
        return changed

    def move(self, direction):
        changed = False
        if direction == "left":
            changed = self.moveLeft()
        elif direction == "right":
            changed = self.moveRight()
        elif direction == "up":
            changed = self.moveUp()
        elif direction == "down":
            changed = self.moveDown()
        # Update empty tiles after every move
        self.emptyTiles = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        self.nEmptyTiles = len(self.emptyTiles)
        self.maxTile = max(max(row) for row in self.grid)
        # Only spawn a tile if the board changed
        if changed:
            self.spawnTile()
        # Check for game over
        if not self.possibleMoves():
            self.gameOver = True

    def spawnTile(self):
        try:
            pos = random.randint(0, self.nEmptyTiles - 1)
            i, j = self.emptyTiles[pos]
            self.grid[i][j] = 2 if random.random() < 0.8 else 4
            self.emptyTiles.remove((i, j))
            self.nEmptyTiles -= 1
        except ValueError:
            self.gameOver = self.possibleMoves()

    def printBoard(self):
        for row in self.grid:
            print(" ".join("{:4}".format(val) if val != 0 else "   ." for val in row))
        print("Score:", self.score)

    def possibleMoves(self):
        # Check for any empty tile
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return True
        # Check for any adjacent tiles with the same value
        for i in range(4):
            for j in range(4):
                if i < 3 and self.grid[i][j] == self.grid[i+1][j]:
                    return True
                if j < 3 and self.grid[i][j] == self.grid[i][j+1]:
                    return True
        return False

# def main(stdscr):
#     board = Board()
#     while True:
#         stdscr.clear()
#         for row in board.grid:
#             stdscr.addstr(" ".join("{:4}".format(val) if val != 0 else "   ." for val in row) + '\n')
#         stdscr.addstr(f"Score: {board.score}\n")
#         stdscr.addstr("Use arrow keys to move. Press 'q' to quit.\n")
#         if board.gameOver:
#             stdscr.addstr(f"Game Over! Final Score: {board.score}\n")
#             stdscr.addstr(f"Max Tile: {board.getMaxTile()}\n")
#             stdscr.addstr("Press 'q' to quit | 'r' to restart.\n")
#         key = stdscr.getch()
#         if key == curses.KEY_LEFT:
#             board.move("left")
#         elif key == curses.KEY_RIGHT:
#             board.move("right")
#         elif key == curses.KEY_UP:
#             board.move("up")
#         elif key == curses.KEY_DOWN:
#             board.move("down")
#         elif key == ord('q'):
#             break
#         elif key == ord('r'):
#             board.reset()

# Genetic Algorithm integration for 2048 using pygad
# Install pygad: pip install pygad

# Map integer genes to moves
move_map = {0: "left", 1: "right", 2: "up", 3: "down"}

def fitness_func(ga_instance, solution, solution_idx):
    board = Board()
    move_idx = 0
    max_loops = 1000  # Prevent infinite loops
    while not board.gameOver and move_idx < max_loops:
        prev_grid = [row[:] for row in board.grid]
        move = move_map[int(solution[move_idx % len(solution)]) % 4]
        board.move(move)
        move_idx += 1
        # If the board didn't change, check for a full cycle
        if board.grid == prev_grid and move_idx % len(solution) == 0:
            break
    return board.score + 10 * board.getMaxTile()

if __name__ == "__main__":
    total_runs = 15  # Change this to set how many times to restart with best solution
    generations_per_run = 50
    population_size = 40
    num_genes = 500
    best_solution = None
    best_score = -float('inf')
    best_tile = 0

    for run in range(total_runs):
        if best_solution is not None:
            initial_population = [best_solution] + [np.random.randint(0, 4, num_genes) for _ in range(population_size-1)]
        else:
            initial_population = None

        ga_instance = pygad.GA(
            num_generations=generations_per_run,
            num_parents_mating=20,
            fitness_func=fitness_func,
            sol_per_pop=population_size,
            num_genes=num_genes,
            gene_type=int,
            init_range_low=0,
            init_range_high=4,
            mutation_percent_genes=10,
            initial_population=initial_population
        )

        ga_instance.run()
        solution, solution_fitness, _ = ga_instance.best_solution()
        # Evaluate max tile for best solution
        board = Board()
        for gene in solution:
            move = move_map[int(gene) % 4]
            board.move(move)
            if board.gameOver:
                break
        max_tile = board.getMaxTile()
        board.printBoard()
        print(f"Run {run+1}: Best score: {board.getScore()}, Max tile: {max_tile}\n")
        if solution_fitness > best_score:
            best_solution = solution
            best_score = solution_fitness
            best_tile = max_tile
    
    # print("Final best sequence:", [move_map[int(g) % 4] for g in best_solution])
    print("Final best score:", best_score)
    print("Final best tile:", best_tile)

# curses.wrapper(main)
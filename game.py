import random
import numpy as np
import pygad
import math
import os

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

# --- Heuristic evaluation function ---
def evaluate_board(board, weights):
    grid = board.getGrid()
    empty_tiles = len(board.getEmptyTiles())
    max_tile = board.getMaxTile()

    # Smoothness: penalty for differences between neighbors
    smoothness = 0
    for i in range(4):
        for j in range(3):
            if grid[i][j] and grid[i][j+1]:
                smoothness -= abs(grid[i][j] - grid[i][j+1])
            if grid[j][i] and grid[j+1][i]:
                smoothness -= abs(grid[j][i] - grid[j+1][i])

    # Monotonicity: reward if values decrease left→right or top→bottom
    monotonicity = 0
    for row in grid:
        for a, b in zip(row, row[1:]):
            if a >= b: monotonicity += 1
    for col in zip(*grid):
        for a, b in zip(col, col[1:]):
            if a >= b: monotonicity += 1

    # Corner max: reward if max tile is in a corner
    corner_max = 1 if max_tile in [
        grid[0][0], grid[0][3], grid[3][0], grid[3][3]
    ] else 0

    features = np.array([
        empty_tiles,
        math.log(max_tile, 2) if max_tile > 0 else 0,
        smoothness,
        monotonicity,
        corner_max
    ])

    return np.dot(weights, features)


# --- Fitness function for GA ---
def fitness_func(ga_instance, solution, solution_idx):
    num_trials = 5
    total_score = 0
    total_max = 0

    for _ in range(num_trials):
        board = Board()
        move_limit = 2000
        for _ in range(move_limit):
            if board.gameOver:
                break

            # Try each move
            best_score = -1e9
            best_move = None
            for move in ["left", "right", "up", "down"]:
                test_board = Board()
                test_board.grid = [row[:] for row in board.grid]
                test_board.score = board.score
                test_board.move(move)
                if test_board.grid != board.grid:  # valid move
                    score = evaluate_board(test_board, solution)
                    if score > best_score:
                        best_score = score
                        best_move = move

            if best_move is None:
                break
            board.move(best_move)

        total_score += board.getScore()
        total_max += board.getMaxTile()

    avg_score = total_score / num_trials
    avg_max = total_max / num_trials
    return avg_score + (avg_max ** 2)


# --- Run GA ---
if __name__ == "__main__":

    num_features = 5
    target_tile = 2048
    run = 0

    while True:
        run += 1
        print(f"\n=== GA Run {run} ===")

        # Load previous best if exists
        if os.path.exists("best_weights.npy"):
            best_weights = np.load("best_weights.npy")
            initial_population = [
                best_weights + np.random.normal(0, 1, size=len(best_weights))
                for _ in range(10)
            ]
            print("Loaded previous best weights:", best_weights)
        else:
            initial_population = None

        # New GA instance for this run
        ga_instance = pygad.GA(
            num_generations=50,
            num_parents_mating=10,
            fitness_func=fitness_func,
            sol_per_pop=30,
            num_genes=num_features,
            gene_type=float,
            init_range_low=-10,
            init_range_high=10,
            mutation_percent_genes=30,
            initial_population=initial_population
        )

        # Train
        ga_instance.run()

        # Get best solution
        solution, fitness, _ = ga_instance.best_solution()
        print("Best weights:", solution)
        print("Best fitness:", fitness)

        # Save best weights
        np.save("best_weights.npy", solution)

        # --- Test the best weights ---
        board = Board()
        move_limit = 5000
        while not board.gameOver and move_limit > 0:
            move_limit -= 1
            best_score = -1e9
            best_move = None
            for move in ["left", "right", "up", "down"]:
                test_board = Board()
                test_board.grid = [row[:] for row in board.grid]
                test_board.score = board.score
                test_board.move(move)
                if test_board.grid != board.grid:
                    score = evaluate_board(test_board, solution)
                    if score > best_score:
                        best_score = score
                        best_move = move
            if best_move is None:
                break
            board.move(best_move)

        print("Final Score:", board.getScore(), "Max tile:", board.getMaxTile())
        board.printBoard()

        if board.getMaxTile() >= target_tile:
            print("Target reached!")
            break

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

# Map integer genes to moves
move_map = {0: "left", 1: "right", 2: "up", 3: "down"}

def fitness_func(ga_instance, solution, solution_idx):
    # Average fitness over multiple random games
    num_trials = 3
    total_score = 0
    total_max_tile = 0
    total_empty_tiles = 0
    for _ in range(num_trials):
        board = Board()
        move_idx = 0
        max_loops = 1000
        while not board.gameOver and move_idx < max_loops:
            prev_grid = [row[:] for row in board.grid]
            move = move_map[int(solution[move_idx % len(solution)]) % 4]
            board.move(move)
            move_idx += 1
            if board.grid == prev_grid and move_idx % len(solution) == 0:
                break
        total_score += board.score
        total_max_tile += board.getMaxTile()
        total_empty_tiles += len(board.getEmptyTiles())
    avg_score = total_score / num_trials
    avg_max_tile = total_max_tile / num_trials
    avg_empty_tiles = total_empty_tiles / num_trials
    # Combine score, max tile, and empty tiles
    return avg_score + (avg_max_tile ** 2) + 5 * avg_empty_tiles

if __name__ == "__main__":
    total_runs = 50
    generations_per_run = 100
    population_size = 100
    num_genes = 500
    num_elites = 5
    best_solutions_ever = []
    best_scores_ever = []
    best_tiles_ever = []
    target_tile = 512  # Set your target tile here

    run = 0

    #for run in range(total_runs):
    while True:
        run += 1
        initial_population = []
        if best_solutions_ever:
            initial_population.extend(best_solutions_ever)
        initial_population += [np.random.randint(0, 4, num_genes) for _ in range(population_size - len(initial_population))]
        if not best_solutions_ever:
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
            mutation_percent_genes=40,
            initial_population=initial_population
        )

        ga_instance.run()
        solutions = ga_instance.population
        fitnesses = ga_instance.last_generation_fitness
        sorted_indices = np.argsort(fitnesses)[::-1]
        best_solutions_ever = [solutions[i] for i in sorted_indices[:num_elites]]
        best_scores_ever = [fitnesses[i] for i in sorted_indices[:num_elites]]
        best_tiles_ever = []
        for elite in best_solutions_ever:
            board = Board()
            move_idx = 0
            max_loops = 1000
            while not board.gameOver and move_idx < max_loops:
                move = move_map[int(elite[move_idx % len(elite)]) % 4]
                board.move(move)
                move_idx += 1
            best_tiles_ever.append(board.getMaxTile())
        print(f"Run {run+1}: Best scores: {best_scores_ever}, Max tiles: {best_tiles_ever}")
        if best_tiles_ever[0] >= target_tile:
            print(f"Target reached: {best_tiles_ever[0]} in run {run+1}")
            break

    print("Final best score:", best_scores_ever[0])
    print("Final best tile:", best_tiles_ever[0])

# curses.wrapper(main)
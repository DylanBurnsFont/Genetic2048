import curses
from random import randint

class Board():
    def __init__(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.emptyTiles = [(i, j) for i in range(4) for j in range(4)]
        self.nEmptyTiles = 16
        self.spawnTile()
        self.gameOver = False
    
    def reset(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.emptyTiles = [(i, j) for i in range(4) for j in range(4)]
        self.nEmptyTiles = 16
        self.spawnTile()
        self.gameOver = False

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
        # Only spawn a tile if the board changed
        if changed:
            self.spawnTile()
        # Check for game over
        if not self.possibleMoves():
            self.gameOver = True

    def spawnTile(self):
        try:
            pos = randint(0, self.nEmptyTiles - 1)
            i, j = self.emptyTiles[pos]
            self.grid[i][j] = 2 if randint(0, 1) == 0 else 4
            self.emptyTiles.remove((i, j))
            self.nEmptyTiles -= 1
        except ValueError:
            self.gameOver = self.possibleMoves()

    def printBoard(self):
        for row in self.grid:
            print(row)
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

def main(stdscr):
    board = Board()
    while True:
        stdscr.clear()
        for row in board.grid:
            stdscr.addstr(str(row) + '\n')
        stdscr.addstr(f"Score: {board.score}\n")
        stdscr.addstr("Use arrow keys to move. Press 'q' to quit.\n")
        if board.gameOver:
            stdscr.addstr(f"Game Over! Final Score: {board.score}\n")
            stdscr.addstr("Press 'q' to quit.\n")
        key = stdscr.getch()
        if key == curses.KEY_LEFT:
            board.move("left")
        elif key == curses.KEY_RIGHT:
            board.move("right")
        elif key == curses.KEY_UP:
            board.move("up")
        elif key == curses.KEY_DOWN:
            board.move("down")
        elif key == ord('q'):
            break

curses.wrapper(main)
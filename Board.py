import collections
import random


class Board:
    board = list
    rows: int
    cols: int
    player_pos: tuple
    moves = collections.defaultdict(tuple)
    boxes: set[tuple]
    holes: set[tuple]

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[' '] * rows for _ in range(cols)]
        self.player_pos = (1, 1)

        self.moves['a'] = (0, -1)
        self.moves['d'] = (0, 1)
        self.moves['w'] = (-1, 0)
        self.moves['s'] = (1, 0)

        self.boxes = set()
        while len(self.boxes) < 5:
            x = random.randint(2, rows - 3)
            y = random.randint(2, cols - 3)
            if (x, y) != self.player_pos and (x, y) not in self.boxes:
                self.boxes.add((x, y))

        self.holes = set()
        while len(self.holes) < 5:
            x = random.randint(2, rows - 3)
            y = random.randint(2, cols - 3)
            if (x, y) != self.player_pos and (x, y) not in self.holes and (x, y) not in self.boxes:
                self.holes.add((x, y))

        self.print()

    def play(self, move):
        if move == 'r':
            self._reset()
        if move not in self.moves:
            return

        nr, nc = self.moves[move]
        nr += self.player_pos[0]
        nc += self.player_pos[1]

        if self.rows - 1 > nr > 0 < nc < self.cols - 1:
            if (nr, nc) in self.boxes:
                if not self._moveBox(nr, nc):
                    return False
            self.player_pos = (nr, nc)
            self.print()

            if len(self.boxes) == 0:
                return True

            return False

    def _moveBox(self, row, col):
        if (row, col) in self.boxes:
            dx, dy = row - self.player_pos[0], col - self.player_pos[1]
            nr, nc = dx + row, dy + col
            if (nr, nc) in self.boxes or not (self.rows - 1 > nr > 0 < nc < self.cols - 1):
                return False

            self.boxes.remove((row, col))

            if (nr, nc) in self.holes:
                self.holes.remove((nr, nc))
            else:
                self.boxes.add((nr, nc))

            return True

    def print(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if i == 0 or i == self.rows - 1 or j == 0 or j == self.cols - 1:
                    print('\u25a9', end=' ')
                elif (i, j) == self.player_pos:
                    print('o', end=' ')
                elif (i, j) in self.boxes:
                    print('\u25a9', end=' ')
                elif (i, j) in self.holes:
                    print('\u2610', end=' ')
                else:
                    print(self.board[i][j], end=' ')
            print()

        if len(self.boxes) == 0:
            print('You Win!')
        else:
            print('Press \'r\' to reset')

    def _reset(self):
        self.__init__(self.rows, self.cols)

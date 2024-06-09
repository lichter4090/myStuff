import random
import sudoku_db


class Board:
    def __init__(self, rows=9, cols=9, board=None, solution=None):
        if rows != cols != 9:
            exit(1)

        self.rows = rows
        self.cols = cols
        self.board = [[0] * self.cols for _ in range(self.rows)]
        self.original_game = [[0] * self.cols for _ in range(self.rows)]
        self.solution = [[0] * self.cols for _ in range(self.rows)]

        if board is not None:
            for i in range(self.rows):
                for j in range(self.cols):
                    self.board[i][j] = int(board[i * self.rows + j])
                    self.original_game[i][j] = int(board[i * self.rows + j])
                    self.solution[i][j] = int(solution[i * self.rows + j])

    def clear_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = 0

    def set_value(self, row_idx, col_idx, value, overwrite=True):
        if self.original_game[row_idx][col_idx] != 0:
            if overwrite:
                self.board[row_idx][col_idx] = value

        else:
            self.board[row_idx][col_idx] = value

    def get_rows(self):
        return self.rows

    def get_cols(self):
        return self.cols

    def check_valid(self, row_idx, col_idx, value):
        if value in self.board[row_idx]:
            return False

        if value in [self.board[i][col_idx] for i in range(self.rows)]:
            return False

        box_x = col_idx // 3
        box_y = row_idx // 3

        for i in range(box_y * 3, box_y * 3 + self.cols // 3):
            for j in range(box_x * 3, box_x * 3 + self.rows // 3):
                if self.board[i][j] == value:
                    return False

        return True

    def find_empty_spot(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == 0:
                    return i, j

    def solve_board(self):
        spot = self.find_empty_spot()

        if spot is None:
            return True

        row, col = spot

        for i in range(1, self.rows + 1):
            if self.check_valid(row, col, i):
                self.board[row][col] = i

                if self.solve_board():
                    return True

                self.board[row][col] = 0

        return False

    def print_board(self, s=False):
        if s:
            a = self.solution
        else:
            a = self.board

        for i in range(self.rows):
            for j in range(self.cols):
                print(a[i][j], end=" ")

            print()

        print()

    def get_board(self):
        return self.board

    def set_board(self, new_board):
        self.board = new_board

    def get_original_game(self):
        return self.original_game

    def print_solution(self):
        self.print_board(True)

    def get_solution(self):
        return self.solution


def get_game():
    db_list = sudoku_db.get_db_list()

    return tuple(random.choice(db_list).split(","))


def main():
    game, solution = get_game()

    board = Board(board=game, solution=solution)

    board.solve_board()

    board.print_board()
    board.print_solution()


if __name__ == "__main__":
    main()

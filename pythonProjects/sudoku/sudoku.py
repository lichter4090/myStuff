import sudoku_solver
import pygame
import time
import pop_allert

info = """
Hello! Welcome to my sudoku game.
If you don't know what is a sudoku go check online please.
Move between cells with arrows or by pressing the cell.
Fill the cells by pressing the numbers in your keyboard.
When filling the sudoku matrix, the numbers will be gray, the meaning is that you are in edit mode.
After pressing enter you will see what cells are correct (red means wrong, black means right).
If you give up you can press space and watch the computer solving the game and start a new game by pressing the key n in the keyboard.

Good Luck!
"""

pygame.init()

SIZE_OF_CELL = 60

WIDTH, HEIGHT = SIZE_OF_CELL * 9, SIZE_OF_CELL * 9

BOX_BORDER_WIDTH = int(SIZE_OF_CELL // 13.4)
CELL_BORDER_WIDTH = int(SIZE_OF_CELL // 16.75)

WINDOW_WIDTH = WIDTH + 12 * CELL_BORDER_WIDTH + 2 * BOX_BORDER_WIDTH
WINDOW_HEIGHT = WINDOW_WIDTH

REAL_WINDOW_HEIGHT = WINDOW_HEIGHT + SIZE_OF_CELL // 2

FPS = 60

WHITE = 255, 255, 255
BLACK = 0, 0, 0
LIGHT_GRAY = 200, 200, 200
GRAY = 150, 150, 150
RED = 255, 0, 0


BOX_BORDER_COLOR = 0, 0, 0

font = pygame.font.Font('freesansbold.ttf', 32)
little_font = pygame.font.Font('freesansbold.ttf', 20)


INFO_RECT = pygame.Rect(WINDOW_WIDTH - SIZE_OF_CELL // 2, WINDOW_HEIGHT, SIZE_OF_CELL // 2, SIZE_OF_CELL // 2)
INFO_TEXT = little_font.render("i", True, BLACK)
HOVERING_INFO_BUTTON = False


class PygameBoard(sudoku_solver.Board):
    def __init__(self, board=None, solution=None):
        super().__init__(board=board, solution=solution)

        self.start_time = time.time()

        self.pygame_rect_board = list()
        self.clicked_rect_idx = -1
        self.error_report = [[True] * self.cols for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                r = pygame.Rect((j + 2) * CELL_BORDER_WIDTH + j * SIZE_OF_CELL + (j // 3) * BOX_BORDER_WIDTH, (i + 2) * CELL_BORDER_WIDTH + i * SIZE_OF_CELL + (i // 3) * BOX_BORDER_WIDTH, SIZE_OF_CELL, SIZE_OF_CELL)
                self.pygame_rect_board.append(r)

    def get_pygame_board(self):
        return self.pygame_rect_board

    def set_clicked_rect_idx(self, value, mouse_click=False):
        if mouse_click:
            self.clicked_rect_idx = value
            return

        if self.clicked_rect_idx == -1:
            self.clicked_rect_idx = 0

        elif 0 <= value < len(self.pygame_rect_board):
            self.clicked_rect_idx = value

    def get_clicked_rect_idx(self):
        return self.clicked_rect_idx

    def check_current_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    continue

                if self.solution[i][j] == self.board[i][j]:
                    self.original_game[i][j] = self.board[i][j]
                    self.error_report[i][j] = True

                else:
                    self.error_report[i][j] = False

    def get_error_report(self):
        return self.error_report

    def pygame_solve_board(self, window, clock):
        spot = self.find_empty_spot()

        if spot is None:
            return True

        row, col = spot

        for i in range(1, self.rows + 1):
            if self.check_valid(row, col, i):
                clock.tick(FPS)
                self.board[row][col] = i

                draw_window(window, self)

                if self.pygame_solve_board(window, clock):
                    return True

                self.board[row][col] = 0

        return False

    def reset_board_to_original_game(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.board[i][j] = self.original_game[i][j]

    def get_start_time(self):
        return self.start_time

    def reset_start_time(self):
        self.start_time = 0


def get_stopwatch(start_time):
    stopwatch = time.time() - start_time
    hours = int(stopwatch // 3600)
    stopwatch %= 3600
    minutes = int(stopwatch // 60)
    stopwatch %= 60

    return f"{hours:02}:{minutes:02}:{int(stopwatch):02}"


def draw_window(window, board):
    pygame.font.init()

    window.fill(WHITE)

    pygame.draw.rect(window, BLACK, pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), CELL_BORDER_WIDTH)

    idx_of_clicked_rect = board.get_clicked_rect_idx()
    pygame_rect_board = board.get_pygame_board()
    for idx, rect in enumerate(pygame_rect_board):  # cells
        if idx == idx_of_clicked_rect:
            color = RED
        else:
            color = LIGHT_GRAY

        pygame.draw.rect(window, color, rect, 3)

    for i in range(1, 3):  # lines of boxes
        x = i * 3 * SIZE_OF_CELL + (i * 3 + CELL_BORDER_WIDTH / 2) * CELL_BORDER_WIDTH + (i - 1) * BOX_BORDER_WIDTH
        r1 = pygame.Rect(x, CELL_BORDER_WIDTH, BOX_BORDER_WIDTH, WINDOW_HEIGHT - CELL_BORDER_WIDTH)  # horizontal line
        r2 = pygame.Rect(CELL_BORDER_WIDTH, x, WINDOW_HEIGHT, BOX_BORDER_WIDTH)  # vertical line

        pygame.draw.rect(window, BLACK, r1)
        pygame.draw.rect(window, BLACK, r2)

    board_nums = board.get_board()
    original_game = board.get_original_game()
    error_report = board.get_error_report()

    for i in range(len(board_nums)):  # numbers
        for j in range(len(board_nums[0])):
            if board_nums[i][j] == 0:
                continue

            if not error_report[i][j]:
                color = RED

            elif original_game[i][j] == 0:
                color = GRAY

            else:
                color = BLACK

            num = font.render(f"{board_nums[i][j]}", True, color)
            text_rect = num.get_rect()
            text_rect.center = pygame_rect_board[i * board.get_cols() + j].center

            window.blit(num, text_rect)

    stopwatch_label = font.render(get_stopwatch(board.get_start_time()), True, BLACK)
    window.blit(stopwatch_label, (CELL_BORDER_WIDTH, WINDOW_HEIGHT + CELL_BORDER_WIDTH))

    if HOVERING_INFO_BUTTON:
        color = LIGHT_GRAY

    else:
        color = WHITE

    pygame.draw.rect(window, color, INFO_RECT)
    pygame.draw.rect(window, BLACK, INFO_RECT, width=CELL_BORDER_WIDTH)

    text_rect = INFO_TEXT.get_rect()
    text_rect.center = INFO_RECT.center
    window.blit(INFO_TEXT, text_rect)

    pygame.display.update()  # update the window


def main():
    global HOVERING_INFO_BUTTON

    window = pygame.display.set_mode((WINDOW_WIDTH, REAL_WINDOW_HEIGHT))
    pygame.display.set_caption("Sudoku")

    game, solution = sudoku_solver.get_game()

    board = PygameBoard(board=game, solution=solution)

    clock = pygame.time.Clock()
    to_exit = False

    while not to_exit:
        clock.tick(FPS)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                to_exit = True

            if INFO_RECT.collidepoint(mouse_x, mouse_y):
                HOVERING_INFO_BUTTON = True
            else:
                HOVERING_INFO_BUTTON = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if INFO_RECT.collidepoint(mouse_x, mouse_y):
                    pop_allert.pop_msg("Info", info)

                for idx, rect in enumerate(board.get_pygame_board()):
                    if rect.collidepoint(mouse_x, mouse_y):
                        board.set_clicked_rect_idx(idx, mouse_click=True)

            if event.type == pygame.KEYDOWN:
                value = 0
                current_idx = board.get_clicked_rect_idx()
                row = current_idx // board.get_cols()
                col = current_idx % board.get_cols()

                if event.key == pygame.K_RIGHT:
                    value += 1

                if event.key == pygame.K_LEFT:
                    value -= 1

                if event.key == pygame.K_UP:
                    value -= board.cols

                if event.key == pygame.K_DOWN:
                    value += board.cols

                if event.key == pygame.K_1:
                    board.set_value(row, col, 1, False)

                if event.key == pygame.K_2:
                    board.set_value(row, col, 2, False)

                if event.key == pygame.K_3:
                    board.set_value(row, col, 3, False)

                if event.key == pygame.K_4:
                    board.set_value(row, col, 4, False)

                if event.key == pygame.K_5:
                    board.set_value(row, col, 5, False)

                if event.key == pygame.K_6:
                    board.set_value(row, col, 6, False)

                if event.key == pygame.K_7:
                    board.set_value(row, col, 7, False)

                if event.key == pygame.K_8:
                    board.set_value(row, col, 8, False)

                if event.key == pygame.K_9:
                    board.set_value(row, col, 9, False)

                if event.key in (pygame.K_0, pygame.K_BACKSPACE, pygame.K_DELETE):
                    board.set_value(row, col, 0, False)

                if event.key == pygame.K_RETURN:
                    board.check_current_board()

                if event.key == pygame.K_SPACE:
                    board.reset_board_to_original_game()
                    board.set_clicked_rect_idx(-1, True)
                    board.pygame_solve_board(window, clock)
                    board.check_current_board()

                if event.key == pygame.K_n:
                    game, solution = sudoku_solver.get_game()
                    board = PygameBoard(board=game, solution=solution)

                board.set_clicked_rect_idx(current_idx + value)

        draw_window(window, board)

    pygame.quit()


if __name__ == "__main__":
    main()

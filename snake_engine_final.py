import pygame
import random

pygame.init()
pygame.font.init()

SIZE_OF_ELEMENT = 36
BODY_PARTS = 3


WINDOW_WIDTH = SIZE_OF_ELEMENT * 15
WINDOW_HEIGHT = WINDOW_WIDTH + SIZE_OF_ELEMENT
FPS = 40
CHANGE_FPS = 10


WHITE = 255, 255, 255
ORANGE = 255, 165, 0
GREEN = 0, 255, 0
BLACK = 0, 0, 0
RED = 255, 0, 0

big_font = pygame.font.Font('freesansbold.ttf', 32)
smaller_font = pygame.font.Font('freesansbold.ttf', 16)

NUM_OF_MOVES_INTO_THE_FUTURE = 30

LOSING_MOVE = -1000
EATING_APPLE = 500
CLOSER_TO_APPLE_POINT = 2
FURTHER_TO_SNAKE = -1

game_frame = pygame.Rect(0, SIZE_OF_ELEMENT, WINDOW_WIDTH, WINDOW_WIDTH)
score_frame = pygame.Rect(0, 0, WINDOW_WIDTH, SIZE_OF_ELEMENT)


class Snake:
    def __init__(self, positions=None, x=0, y=SIZE_OF_ELEMENT, direction=(0, 1)):
        self.x = x
        self.y = y
        self.direction = direction
        self.positions = positions
        self.score = 0

        if positions is None:
            self.positions = [(0, SIZE_OF_ELEMENT) for _ in range(BODY_PARTS)]
        else:
            self.positions = positions

    def set_coordinates(self, coordinates):
        self.x, self.y = coordinates

    def set_direction(self, direction):
        self.direction = direction

    def pop_last(self):
        self.positions.pop(-1)

    def add_position(self, position):
        self.positions.insert(0, position)

    def get_coordinates(self):
        return self.x, self.y

    def get_positions(self):
        return self.positions

    def get_direction(self):
        return self.direction

    def draw(self, window):
        is_head = True

        for x, y in self.positions:
            if is_head:
                color = ORANGE
                is_head = False
            else:
                color = GREEN

            r = pygame.Rect(x, y, SIZE_OF_ELEMENT, SIZE_OF_ELEMENT)
            pygame.draw.rect(window, color, r, width=2)

    def check_if_snake_ate_food(self, food):
        if self.get_coordinates() == food.get_coordinates():
            self.score += 1
            return True

        return False

    def move(self):
        self.x += self.direction[0] * SIZE_OF_ELEMENT
        self.y += self.direction[1] * SIZE_OF_ELEMENT

        self.add_position((self.x, self.y))

    def check_collisions(self):
        if self.x < 0 or self.x >= WINDOW_WIDTH:
            return True
        elif self.y < SIZE_OF_ELEMENT or self.y >= WINDOW_HEIGHT:
            return True
        elif (self.x, self.y) in self.positions[1:]:
            return True

        return False

    def get_score(self):
        return self.score


class Food:
    def __init__(self, x=-1, y=-1):
        if -1 in (x, y):
            self.x = random.randint(0, (WINDOW_WIDTH // SIZE_OF_ELEMENT) - 1) * SIZE_OF_ELEMENT
            self.y = random.randint(1, (WINDOW_WIDTH // SIZE_OF_ELEMENT) - 1) * SIZE_OF_ELEMENT
        else:
            self.x = x
            self.y = y

    def get_coordinates(self):
        return self.x, self.y

    def set_coordinates(self, coordinates):
        self.x, self.y = coordinates

    def return_center(self):
        return self.x + SIZE_OF_ELEMENT // 2, self.y + SIZE_OF_ELEMENT // 2

    def draw(self, window):
        pygame.draw.circle(window, RED, self.return_center(), SIZE_OF_ELEMENT // 2)


def check_if_move_possible(current_snake, new_direction):
    try:
        index = current_snake.get_direction().index(1)
    except ValueError:
        index = current_snake.get_direction().index(-1)

    return current_snake.get_direction()[index] == new_direction[index] or new_direction[index] == 0
    # if the 1/-1 in the directions are the same (both 1 and not -1 or the opposite)


def get_move_to_play(snake, apple, iteration):
    lst_of_moves = list()
    lst_of_points_check_valid = list()

    for i in (-1, 1):  # checks the valid moves
        if check_if_move_possible(snake, (0, i)):
            lst_of_moves.append((0, i))
            lst_of_points_check_valid.append(0)

        if check_if_move_possible(snake, (i, 0)):
            lst_of_moves.append((i, 0))
            lst_of_points_check_valid.append(0)

    x, y = snake.get_coordinates()
    last_positions = list(snake.get_positions())

    for idx, move in enumerate(lst_of_moves):  # check each move if it is not losing
        new_x = x + move[0] * SIZE_OF_ELEMENT
        new_y = y + move[1] * SIZE_OF_ELEMENT

        snake.set_coordinates((new_x, new_y))

        if snake.check_collisions():
            lst_of_points_check_valid[idx] = LOSING_MOVE

    snake.set_coordinates((x, y))  # reset snake to its original position

    lst_of_valid_moves = [move for idx, move in enumerate(lst_of_moves) if lst_of_points_check_valid[idx] != LOSING_MOVE]
    # create a list of only the moves that doesn't lose

    lst_of_points = [0] * len(lst_of_valid_moves)

    if len(lst_of_valid_moves) == 0:
        return lst_of_moves[0], LOSING_MOVE

    if apple is not None:
        apple_x, apple_y = apple.get_coordinates()
        trying_food = Food(apple_x, apple_y)
        for idx, move in enumerate(lst_of_valid_moves):
            new_x = x + move[0] * SIZE_OF_ELEMENT
            new_y = y + move[1] * SIZE_OF_ELEMENT

            if abs(x - apple_x) > abs(new_x - apple_x) or abs(y - apple_y) > abs(new_y - apple_y):
                lst_of_points[idx] += CLOSER_TO_APPLE_POINT

            if new_x == apple_x and new_y == apple_y:
                lst_of_points[idx] += EATING_APPLE

    else:
        apple_x, apple_y = -1, -1
        trying_food = None

    idx_of_best_move = lst_of_points.index(max(lst_of_points))
    best_move = lst_of_valid_moves[idx_of_best_move]
    found_move = False

    if iteration < NUM_OF_MOVES_INTO_THE_FUTURE:
        next_move_idx = -2
        while not found_move:
            new_x = x + best_move[0] * SIZE_OF_ELEMENT
            new_y = y + best_move[1] * SIZE_OF_ELEMENT

            new_positions = list(last_positions)
            new_positions.insert(0, (new_x, new_y))

            if not (new_x == apple_x and new_y == apple_y):
                new_positions.pop(-1)
            else:
                trying_food = None

            trying_snake = Snake(positions=new_positions, x=new_x, y=new_y, direction=best_move)
            result = get_move_to_play(trying_snake, trying_food, iteration + 1)[1]

            if result != LOSING_MOVE:
                found_move = True
            else:
                try:
                    best_move = lst_of_valid_moves[lst_of_points.index(sorted(lst_of_points)[next_move_idx])]
                    next_move_idx -= 1
                except IndexError:
                    return best_move, LOSING_MOVE

    return best_move, lst_of_points[idx_of_best_move]


def draw_text(window, text, center_coordinates, font, color):
    label = font.render(text, True, color)
    text_rect = label.get_rect()
    text_rect.center = center_coordinates
    window.blit(label, text_rect)


def draw_window(window, snake, food, game_over, show_game_over_screen=True):
    #  start drawing
    window.fill(BLACK)

    pygame.draw.rect(window, WHITE, score_frame, width=2)
    pygame.draw.rect(window, BLACK, game_frame)

    if game_over and show_game_over_screen:
        game_over_label = big_font.render("GAME OVER", True, RED)
        text_rect = game_over_label.get_rect()
        text_rect.center = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        window.blit(game_over_label, text_rect)
    else:
        snake.draw(window)
        food.draw(window)

        if game_over:
            draw_text(window, "Finished simulation", (WINDOW_WIDTH // 6, 1.5 * SIZE_OF_ELEMENT), smaller_font, WHITE)

    draw_text(window, f"Score: {snake.get_score()}", (WINDOW_WIDTH // 2, SIZE_OF_ELEMENT // 2), big_font, WHITE)
    draw_text(window, f"FPS: {FPS}", (WINDOW_WIDTH // 6 * 5, SIZE_OF_ELEMENT // 2), big_font, WHITE)
    draw_text(window, f"Moves to the future: {NUM_OF_MOVES_INTO_THE_FUTURE}", (WINDOW_WIDTH // 6, SIZE_OF_ELEMENT // 2), smaller_font, WHITE)

    pygame.display.update()


def main(moves=None):
    global FPS, NUM_OF_MOVES_INTO_THE_FUTURE

    # Set up the window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake")

    snake = Snake()
    food = Food()
    clock = pygame.time.Clock()
    to_exit = False
    game_over = False
    show_game_over_screen = True

    i = 0

    while not to_exit:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                to_exit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    to_exit = True

                if event.key == pygame.K_RIGHT:
                    FPS += CHANGE_FPS

                if event.key == pygame.K_LEFT:
                    FPS -= CHANGE_FPS

                    if FPS < CHANGE_FPS:
                        FPS = CHANGE_FPS

                if event.key == pygame.K_UP:
                    NUM_OF_MOVES_INTO_THE_FUTURE += 5

                if event.key == pygame.K_DOWN:
                    NUM_OF_MOVES_INTO_THE_FUTURE -= 5

                    if NUM_OF_MOVES_INTO_THE_FUTURE < 0:
                        NUM_OF_MOVES_INTO_THE_FUTURE = 0

                if event.key == pygame.K_r:
                    snake = Snake()
                    food = Food()
                    FPS = 40
                    game_over = False

        if not game_over:
            if moves is None:
                snake.set_direction(get_move_to_play(snake, food, 0)[0])
            else:
                try:
                    food.set_coordinates(moves[i][1])

                except IndexError:
                    game_over = True
                    show_game_over_screen = False
                    continue

                snake.set_direction(moves[i][0])
                i += 1

            snake.move()

            game_over = snake.check_collisions()

            # Check if the snake eats the food
            if snake.check_if_snake_ate_food(food):
                if moves is None:
                    food = Food()

                    while food.get_coordinates() in snake.get_positions():
                        food = Food()
                else:
                    try:
                        food.set_coordinates(moves[i][1])

                    except IndexError:
                        game_over = True
                        show_game_over_screen = False
                        continue

            else:
                # Remove the tail of the snake
                snake.pop_last()

        draw_window(window, snake, food, game_over, show_game_over_screen)

    pygame.quit()

    return snake.get_score()


def parse_file_and_get_moves():
    with open("moves.txt", "r") as file:
        moves = file.read().split("\n")[:-1]

        for idx, value in enumerate(moves):
            a = value.split("|")
            move = a[0].split(",")
            apple = a[1].split(",")

            for i in range(2):
                move[i] = int(move[i])
                apple[i] = int(apple[i])

            moves[idx] = tuple(move), tuple(apple)

    return moves


def simulate_game(iteration, snake1=None, food1=None, get_score=False):
    if snake1 is not None:
        snake = snake1
        food = food1

    else:
        snake = Snake()
        food = Food()

    game_over = False
    moves = list()
    i = 0

    try:
        while not game_over and i < iteration:
            #  print(i)
            i += 1
            snake.set_direction(get_move_to_play(snake, food, 0)[0])
            snake.move()

            game_over = snake.check_collisions()

            moves.append((snake.get_direction(), food.get_coordinates()))

            # Check if the snake eats the food
            if snake.check_if_snake_ate_food(food):
                food = Food()  # reset the food variable

                while food.get_coordinates() in snake.get_positions():
                    food = Food()

            else:
                # Remove the tail of the snake
                snake.pop_last()
    except KeyboardInterrupt:
        pass

    if get_score:
        return snake.get_score()

    if i < iteration:
        print("Failed")
        return list()
    else:
        print("Finished")
    return moves


def save_moves(moves, mode="w"):
    with open("moves.txt", mode) as file:
        for move, apple in moves:
            file.write(f"{move[0]},{move[1]}|{apple[0]},{apple[1]}\n")


def play_game():
    """
    function plays the game in the moves.txt file
    :return: the snake and the food after all the game
    :rtype: tuple
    """
    moves = parse_file_and_get_moves()

    snake = Snake()
    food = Food()

    i = 0
    game_over = False

    try:
        while not game_over:
            food.set_coordinates(moves[i][1])

            if moves is None:
                snake.set_direction(get_move_to_play(snake, food, 0)[0])
            else:
                snake.set_direction(moves[i][0])
                i += 1

            snake.move()

            game_over = snake.check_collisions()

            # Check if the snake eats the food
            if snake.check_if_snake_ate_food(food):
                food.set_coordinates(moves[i][1])

            else:
                # Remove the tail of the snake
                snake.pop_last()

    except Exception:
        pass

    return snake, food


def options(option, iteration):
    if option == 0:
        a1 = simulate_game(iteration)
        save_moves(a1)

    elif option == 1:
        return main(parse_file_and_get_moves())

    elif option == 2:
        snake, food = play_game()

        a = simulate_game(iteration, snake, food)
        save_moves(a, "a")


if __name__ == "__main__":
    """
    with open("data.txt", "w") as data_file:
        for n in range(0, 16, 5):
            NUM_OF_MOVES_INTO_THE_FUTURE = n
            print(n)
            for _ in range(3):
                s = simulate_game(1000000, get_score=True) - BODY_PARTS
                data_file.write(f"{n}|{s}\n")
    """

    main()

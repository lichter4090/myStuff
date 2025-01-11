import tkinter as tk
import random
import time

SIZE_OF_ELEMENT = 35
GAME_WIDTH = 525
GAME_HEIGHT = 525
WAITING_TIME = 100
CHECKING_TIME = 1
TEXT_SIZE = 20
BC = "black"
FOOD_COLOR = "red"
SNAKE_COLOR = "green"
HEAD_COLOR = "orange"
BODY_PARTS = 3
BTN_HEIGHT = 1
BTN_WIDTH = 10
BTN_X = 190
BTN_Y = 90

score = 0
lst_of_moves = list()


class Snake:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = (0, 1)
        self.positions = []

        for i in range(BODY_PARTS):
            self.positions.append((0, 0))

    def set_coordinates(self, coordinates):
        self.x, self.y = coordinates

    def set_direction(self, direction):
        self.direction = direction

    def pop_last(self):
        self.positions.pop(-1)

    def add_position(self, position):
        self.positions.insert(0, position)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_coordinates(self):
        return self.x, self.y

    def get_positions(self):
        return self.positions

    def get_direction(self):
        return self.direction


class Food:
    def __init__(self):
        self.x = random.randint(0, (GAME_WIDTH // SIZE_OF_ELEMENT) - 1) * SIZE_OF_ELEMENT
        self.y = random.randint(0, (GAME_HEIGHT // SIZE_OF_ELEMENT) - 1) * SIZE_OF_ELEMENT

    def get_coordinates(self):
        return self.x, self.y

    def set_coordinates(self, coordinates):
        self.x, self.y = coordinates


def check_if_snake_ate_food(current_snake, current_food):
    return current_snake.get_coordinates() == current_food.get_coordinates()


def check_collisions(snake):
    x, y = snake.get_coordinates()

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    elif (x, y) in snake.get_positions()[1:]:
        return True

    return False


def draw_snake(current_snake, canvas):
    is_head = True

    for x, y in current_snake.get_positions():
        if is_head:
            color = HEAD_COLOR
            is_head = False
        else:
            color = SNAKE_COLOR

        canvas.create_rectangle(x,
                                y,
                                x + SIZE_OF_ELEMENT,
                                y + SIZE_OF_ELEMENT,
                                fill=color)


def game(window, current_snake, food, canvas, text_label):
    global score, lst_of_moves

    # Get the current head position of the snake
    current_x, current_y = current_snake.get_coordinates()

    if len(lst_of_moves) != 0:
        current_snake.set_direction(lst_of_moves[0])
        lst_of_moves.pop(0)

    snake_direction = current_snake.get_direction()

    # set the new head position based on the direction
    current_snake.set_coordinates(
        (current_x + snake_direction[0] * SIZE_OF_ELEMENT, current_y + snake_direction[1] * SIZE_OF_ELEMENT))

    if check_collisions(current_snake):
        game_over(window, canvas)
        return

    # Add the new head to the snake's position
    current_snake.add_position(current_snake.get_coordinates())

    # Check if the snake eats the food
    if check_if_snake_ate_food(current_snake, food):
        score += 1

        food = Food()

        while food.get_coordinates() in current_snake.get_positions():
            food = Food()
    else:
        # Remove the tail of the snake
        current_snake.pop_last()

    # Clear the canvas
    canvas.delete("all")

    # Draw the snake
    draw_snake(current_snake, canvas)

    # Draw the food
    canvas.create_oval(food.get_coordinates()[0],
                       food.get_coordinates()[1],
                       food.get_coordinates()[0] + SIZE_OF_ELEMENT,
                       food.get_coordinates()[1] + SIZE_OF_ELEMENT,
                       fill=FOOD_COLOR)

    # Update the score
    text_label.config(text=f"Score: {score}")

    # Schedule the next move
    canvas.after(WAITING_TIME, lambda: game(window, current_snake, food, canvas, text_label))


def check_if_move_possible(current_snake, new_direction):
    try:
        index = current_snake.get_direction().index(1)
    except ValueError:
        index = current_snake.get_direction().index(-1)

    return current_snake.get_direction()[index] == new_direction[index] or new_direction[
        index] == 0  # if the 1/-1 in the directions are the same (both 1 and not -1 or the opposite)


# Function to handle key presses
def handle_keypress(event, snake):
    global lst_of_moves

    if event.keysym == "Up":
        direction = (0, -1)
    elif event.keysym == "Down":
        direction = (0, 1)
    elif event.keysym == "Left":
        direction = (-1, 0)
    elif event.keysym == "Right":
        direction = (1, 0)
    else:
        return

    if check_if_move_possible(snake, direction):
        if snake.get_direction() != direction:
            lst_of_moves.append(direction)


# Function to end the game
def game_over(window, canvas):
    canvas.delete("all")
    canvas.create_text(GAME_WIDTH / 2,
                       GAME_HEIGHT / 2,
                       text="Game Over!",
                       font=("Helvetica", 24),
                       fill="red",
                       anchor="center")
    window.update()
    time.sleep(2)

    window.destroy()


def destroy_btn_and_start_game(window, snake, food, canvas, label, button):
    button.destroy()

    game(window, snake, food, canvas, label)


def play():
    global score, lst_of_moves
    score = 0
    lst_of_moves = list()

    window = tk.Tk()
    window.resizable(False, False)
    window.title("Snake Game")

    score_label = tk.Label(window, text=f"Welcome!", font=("consolas", TEXT_SIZE))
    canvas = tk.Canvas(window, width=GAME_WIDTH, height=GAME_HEIGHT, bg=BC)

    score_label.pack()
    canvas.pack()

    window.update()

    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    window.geometry(f"{width}x{height}+{x}+{y}")
    snake = Snake()
    food = Food()

    start_button = tk.Button(canvas, text="Start Game", font=("consolas", TEXT_SIZE), height=BTN_HEIGHT,
                             width=BTN_WIDTH,
                             command=lambda: destroy_btn_and_start_game(window, snake, food, canvas, score_label, start_button))
    start_button.place(x=BTN_X, y=BTN_Y)

    # Bind the keypress event to the window
    window.bind("<KeyPress>", lambda event: handle_keypress(event, snake))

    # Run the Tkinter event loop
    window.mainloop()

    return score


if __name__ == "__main__":
    play()

from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 200
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

paused = False
game_running = False


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE,
            fill=FOOD_COLOR, tag="food"
        )


def start_game(event=None):
    global snake, food, game_running, score, direction, paused

    canvas.delete(ALL)
    paused = False
    game_running = True

    score = 0
    direction = 'down'
    label.config(text=f"Score: {score}")

    snake = Snake()
    food = Food()

    next_turn(snake, food)


def next_turn(snake, food):
    if not game_running:
        return

    if paused:
        return

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
    )
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def toggle_pause(event=None):
    global paused

    if not game_running:
        return

    if paused:
        resume_game()
    else:
        pause_game()


def pause_game():
    global paused
    paused = True

    canvas.create_text(
        GAME_WIDTH / 2, GAME_HEIGHT / 2 - 30,
        text="PAUSED", fill="white",
        font=("consolas", 50), tag="pause_text"
    )

    canvas.create_text(
        GAME_WIDTH / 2, GAME_HEIGHT / 2 + 20,
        text="Press P to Resume", fill="yellow",
        font=("consolas", 20), tag="pause_text"
    )

    canvas.create_text(
        GAME_WIDTH / 2, GAME_HEIGHT / 2 + 60,
        text="Press R to Restart", fill="orange",
        font=("consolas", 20), tag="pause_text"
    )


def resume_game():
    global paused
    paused = False
    canvas.delete("pause_text")
    next_turn(snake, food)


def restart(event=None):
    start_game()


def change_direction(new_direction):
    global direction

    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    global game_running
    game_running = False

    canvas.delete(ALL)

    canvas.create_text(
        GAME_WIDTH / 2, GAME_HEIGHT / 2 - 20,
        font=('consolas', 60),
        text="GAME OVER",
        fill="red"
    )

    canvas.create_text(
        GAME_WIDTH / 2, GAME_HEIGHT / 2 + 40,
        font=('consolas', 30),
        text="Press R to Restart",
        fill="yellow"
    )


window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text=f"Score: {score}", font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Key bindings
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

window.bind('p', toggle_pause)
window.bind('P', toggle_pause)

window.bind('r', restart)
window.bind('R', restart)

window.bind('s', start_game)
window.bind('S', start_game)

# Start Screen
canvas.create_text(
    GAME_WIDTH / 2, GAME_HEIGHT / 2 - 20,
    text="SNAKE GAME", fill="white",
    font=("consolas", 50)
)

canvas.create_text(
    GAME_WIDTH / 2, GAME_HEIGHT / 2 + 40,
    text="Press S to Start", fill="yellow",
    font=("consolas", 30)
)

window.mainloop()

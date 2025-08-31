import tkinter as tk
import random

GAME_WIDTH = 400
GAME_HEIGHT = 400
SPEED = 100
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
APPLE_COLOR = "#FF0000"
BG_COLOR = "#000000"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

class Apple:
    def __init__(self, canvas, snake):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        while [x, y] in snake.coordinates:
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        self.apple = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=APPLE_COLOR, tag="apple")

def next_turn(snake, apple, canvas, direction, score_label, root):
    x, y = snake.coordinates[0]
    if direction[0] == "up":
        y -= SPACE_SIZE
    elif direction[0] == "down":
        y += SPACE_SIZE
    elif direction[0] == "left":
        x -= SPACE_SIZE
    elif direction[0] == "right":
        x += SPACE_SIZE
    new_head = [x, y]
    snake.coordinates.insert(0, new_head)
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)
    if x == apple.coordinates[0] and y == apple.coordinates[1]:
        canvas.delete("apple")
        apple.__init__(canvas, snake)
        score = int(score_label["text"].split(": ")[1]) + 1
        score_label.config(text=f"Score: {score}")
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    if check_collisions(snake):
        game_over(canvas, root)
    else:
        root.after(SPEED, next_turn, snake, apple, canvas, direction, score_label, root)

def change_direction(new_direction, direction):
    opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
    if new_direction != opposites.get(direction[0]):
        direction[0] = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over(canvas, root):
    canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2, font=('consolas', 30), fill='red', text="GAME OVER")

def main():
    root = tk.Tk()
    root.title("Snake Game")
    root.resizable(False, False)
    score_label = tk.Label(root, text="Score: 0", font=('consolas', 16))
    score_label.pack()
    canvas = tk.Canvas(root, bg=BG_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
    canvas.pack()
    direction = ["right"]
    snake = Snake()
    for x, y in snake.coordinates:
        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
        snake.squares.append(square)
    apple = Apple(canvas, snake)
    root.bind("<Up>", lambda event: change_direction("up", direction))
    root.bind("<Down>", lambda event: change_direction("down", direction))
    root.bind("<Left>", lambda event: change_direction("left", direction))
    root.bind("<Right>", lambda event: change_direction("right", direction))
    next_turn(snake, apple, canvas, direction, score_label, root)
    root.mainloop()

if __name__ == "__main__":
    main()

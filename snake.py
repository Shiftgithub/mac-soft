from turtle import *
from random import randint
from freegames import square, vector

food = vector(0, 0)
snake = [vector(0, 0)]
target = vector(0, 10)


def draw_object(obj, color):
    square(obj.x, obj.y, 9, color)


def inside(head):
    return -200 < head.x < 190 and -200 < head.y < 190


class Snake:
    def __init__(self):
        self.head = snake[-1].copy()
        self.body = snake[:-1]

    def move(self):
        self.body.append(self.head.copy())
        self.head.move(target)

        if not inside(self.head) or self.head in self.body:
            draw_object(self.head, 'red')
            return False

        if self.head == food:
            print('Snake:', len(self.body) + 1)
            food.x = randint(-15, 15) * 10
            food.y = randint(-15, 15) * 10
        else:
            self.body.pop(0)

        return True


def change(x, y):
    target.x = x
    target.y = y


def game_loop(snake):
    if snake.move():
        clear()
        for body_part in snake.body:
            draw_object(body_part, 'black')
        draw_object(snake.head, 'black')
        draw_object(food, 'green')
        update()
        ontimer(lambda: game_loop(snake), 100)


try:
    setup(420, 420, 870, 170)
    hideturtle()
    tracer(False)
    listen()
    onkey(lambda: change(10, 0), 'Right')
    onkey(lambda: change(-10, 0), 'Left')
    onkey(lambda: change(0, 10), 'Up')
    onkey(lambda: change(0, -10), 'Down')
    snake = Snake()
    game_loop(snake).mainloop()
except Exception as e:
    print(e)
    done()

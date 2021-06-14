from turtle import Turtle
from random import choice as random_choice

GAME_HEIGHT = 800  # max ycor: 400, min ycor: -400 | GAME_HEIGHT / 2, in other words.
GAME_WIDTH = 1200
BALL_SIZE = 0.75


class Paddle(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        # I'm setting the heading because when I say width I wanna get width lmao.
        # If the heading is 0 stretch width stretches the length which is ASS.
        self.setheading(90)
        self.shape('square')
        self.color('green')
        self.shapesize(stretch_wid=(BALL_SIZE * 5), stretch_len=BALL_SIZE)
        self.goto(x=0, y=(-GAME_HEIGHT / 2 + 30))
        self.speed('fastest')
        self.showturtle()


class Enemy(Turtle):
    def __init__(self):
        super().__init__()
        self.setheading(90)
        self.shape('square')
        self.color(random_choice(['red', 'green', 'blue']))
        self.shapesize(stretch_wid=(BALL_SIZE * 5), stretch_len=BALL_SIZE)
        self.hideturtle()
        self.penup()
        self.showturtle()
        # magic:
        self.alive = True

    def kill(self):
        self.alive = False
        self.hideturtle()
        print("POW")


class Enemies:
    MARGIN_WIDTH = 0.05 * GAME_WIDTH
    MARGIN_HEIGHT = 0.025 * GAME_HEIGHT
    lines = 5
    turtles_per_line = 12

    @staticmethod
    def float_range(start: float, stop: float, elements: int) -> list:
        numbers = [start]
        number = start
        step = (stop - start) / (elements - 1)
        while len(numbers) != elements:
            number += step
            numbers.append(round(number, 2))
        return numbers
        # I figure the best way to arrange the enemies is through two ranges of floating point numbers:
        # one representing x coordinates and one y coordinates.

    def __init__(self):
        self.list = []
        self.x_cords = self.float_range(start=(-GAME_WIDTH / 2 + self.MARGIN_WIDTH),
                                        stop=(GAME_WIDTH / 2 - self.MARGIN_WIDTH),
                                        elements=self.turtles_per_line)
        self.y_cords = self.float_range(start=(GAME_HEIGHT / 2 - self.MARGIN_HEIGHT),
                                        stop=(GAME_HEIGHT / 2 - self.MARGIN_HEIGHT * self.lines),
                                        elements=self.lines)
        for i in range((self.lines * self.turtles_per_line)):
            enemy = Enemy()
            enemy.goto(x=self.x_cords[i % self.turtles_per_line],
                       y=self.y_cords[i // self.turtles_per_line])
            self.list.append(enemy)


class Ball(Turtle):
    def __init__(self, x_motion: float, y_motion: float):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.shape('circle')
        self.shapesize(BALL_SIZE, BALL_SIZE)
        self.color('black')
        self.speed('fastest')
        self.showturtle()
        self.x_motion = x_motion
        self.y_motion = y_motion

    def move(self):
        self.goto(self.xcor() + self.x_motion, self.ycor() + self.y_motion)


class CollisionDetector:
    def __init__(self, ball: Ball, paddle: Paddle, enemies: Enemies):
        self.ball = ball
        self.paddle = paddle
        self.enemies = enemies

    @staticmethod
    def find_largest_smaller_index(coordinate: float, coord_range: list) -> int:
        if len(coord_range) == 1:
            return coord_range[0]
        delta = coord_range[1] - coord_range[0]
        return (coordinate - coord_range[0]) // delta

    def collision_with_walls(self):
        SENSITIVITY = 5
        if (self.ball.xcor() >= GAME_WIDTH / 2 - SENSITIVITY) or (self.ball.xcor() <= -GAME_WIDTH / 2 + SENSITIVITY):
            self.ball.x_motion *= -1
        if (self.ball.ycor() >= GAME_HEIGHT / 2 - SENSITIVITY) or (self.ball.ycor() <= -GAME_HEIGHT / 2 + SENSITIVITY):
            self.ball.y_motion *= -1

    def collision_with_paddle(self):
        SENSITIVITY_Y = 10
        SENSITIVITY_X = 40
        if (self.paddle.ycor() - SENSITIVITY_Y) <= self.ball.ycor() <= (self.paddle.ycor() + SENSITIVITY_Y):
            if (self.paddle.xcor() - SENSITIVITY_X) <= self.ball.xcor() <= (self.paddle.xcor() + SENSITIVITY_X):
                self.ball.x_motion *= -1
                self.ball.y_motion *= -1

    def collision_with_enemy(self):
        SENSITIVITY_Y = 10
        SENSITIVITY_X = 40
        if self.enemies.y_cords[-1] - SENSITIVITY_Y <= self.ball.ycor() <= self.enemies.y_cords[0] + SENSITIVITY_Y:
            # that means we're close to the enemies in general.
            # y coord of closest enemy:
            y_index_1 = self.find_largest_smaller_index(self.ball.ycor(), self.enemies.y_cords)
            x_index_1 = self.find_largest_smaller_index(self.ball.xcor(), self.enemies.x_cords)
            y_index_2 = y_index_1 if (y_index_1 == (len(self.enemies.y_cords) - 1)) else y_index_1 + 1
            x_index_2 = x_index_1 if (x_index_1 == (len(self.enemies.x_cords) - 1)) else x_index_1 + 1
            for x_index in [x_index_1, x_index_2]:
                for y_index in [y_index_1, y_index_2]:
                    enemy = self.enemies.list[int(y_index * self.enemies.turtles_per_line + x_index)]
                    if enemy.ycor() - SENSITIVITY_Y <= self.ball.ycor() <= enemy.ycor() + SENSITIVITY_Y:
                        if enemy.xcor() - SENSITIVITY_X <= self.ball.xcor() <= enemy.xcor() + SENSITIVITY_X:
                            if enemy.alive:
                                enemy.kill()
                                self.ball.x_motion *= -1
                                self.ball.y_motion *= -1

    def collision_detection(self):
        self.collision_with_walls()
        self.collision_with_paddle()
        self.collision_with_enemy()

from turtle import Turtle
import random

SCREEN_HEIGHT = 800
SCREEN_WIDTH = 800
PLAYER_SIZE_TUPLE = (1, 3)


class GameObject(Turtle):
    def __init__(self, initial_x: float, initial_y: float):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.goto(initial_x, initial_y)
        self.showturtle()
        self.setheading(0)


class Bullet(GameObject):
    def __init__(self, initial_x, initial_y):
        super().__init__(initial_x, initial_y)
        self.shapesize(PLAYER_SIZE_TUPLE[0] / 3)
        self.shape('circle')
        self.color(0.5, 0.7, 0.4)
        self.speed('fastest')


class Player(GameObject):
    def __init__(self, initial_x, initial_y):
        super().__init__(initial_x, initial_y)
        self.shape('square')
        self.shapesize(*PLAYER_SIZE_TUPLE)
        self.cannon = GameObject(initial_x=initial_x, initial_y=(initial_y + PLAYER_SIZE_TUPLE[1] * 5))
        self.cannon.shape('square')
        self.cannon.shapesize(*tuple([element / 2 for element in PLAYER_SIZE_TUPLE]))
        self.cannon.setheading(90)
        self.bullets = []

    def shoot(self):
        bullet = Bullet(self.xcor(), self.ycor())
        bullet.setheading(self.cannon.heading())
        self.bullets.append(bullet)

    def clean_bullets(self):
        for bullet in self.bullets[-1::-1]:
            # The bullets are appended to the list of bullets. The last bullet is the furthest from the
            # the player. The second we encounter a bullet that is within bounds, we're done - all the others
            # are even closer than it.
            if bullet.ycor() <= SCREEN_HEIGHT / 2:
                return
            # Now we clean up the bullets out of bounds.
            bullet.hideturtle()
            self.bullets.pop()

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.forward(50)
        self.clean_bullets()

    def move_player(self, direction):
        if direction == 'right':
            movement = 50
        else:
            movement = -50
        self.goto(self.xcor() + movement, self.ycor())
        self.cannon.goto(self.cannon.xcor() + movement, self.cannon.ycor())


class Enemy(GameObject):
    def __init__(self, initial_x, initial_y):
        super().__init__(initial_x, initial_y)
        self.shape('square')
        self.shapesize(*tuple(element / 2 for element in PLAYER_SIZE_TUPLE))


class Enemies:
    MOVEMENT_CONSTANT = 50
    ENEMIES_PER_LINE = 6
    ENEMY_LINES = 3

    @staticmethod
    def float_range(start: float, stop: float, num_elements: int) -> list:
        numbers = [start]
        number = start
        step = (stop - start) / (num_elements - 1)
        while len(numbers) != num_elements:
            number += step
            numbers.append(round(number, 2))
        return numbers

    def __init__(self):
        x_cords = self.float_range(start=(-SCREEN_WIDTH / 2 + SCREEN_WIDTH / 10),
                                   stop=(SCREEN_WIDTH / 2 - SCREEN_WIDTH / 10),
                                   num_elements=self.ENEMIES_PER_LINE)
        y_cords = self.float_range(start=(SCREEN_HEIGHT / 2 - SCREEN_HEIGHT / 10),
                                   stop=(SCREEN_HEIGHT / 2 - SCREEN_HEIGHT / 40),
                                   num_elements=self.ENEMY_LINES)
        self.enemies_list = []
        for i in range(len(y_cords)):
            for j in range(len(x_cords)):
                enemy = Enemy(initial_x=x_cords[j], initial_y=y_cords[i])
                # the line below is so that the enemies oscillate about a point instead of moving
                # from the starting position and back to it. I want them to oscillate about
                # the 'natural' starting position.
                enemy.goto(x=enemy.xcor() - self.MOVEMENT_CONSTANT / 2, y=enemy.ycor())
                self.enemies_list.append(enemy)
        self.current_direction = 1  # 1 === right, -1 === left
        self.reverse_counter = 0
        self.bullets = []

    def move(self):
        for enemy in self.enemies_list:
            enemy.goto(x=enemy.xcor() + self.current_direction * self.MOVEMENT_CONSTANT / 5,
                       y=enemy.ycor())
        self.reverse_counter += 1
        if self.reverse_counter == 5:
            self.current_direction *= -1
            self.reverse_counter = 0

    def kill(self, particular_enemy: Enemy):
        particular_enemy.hideturtle()
        self.enemies_list.remove(particular_enemy)

    def shoot(self):
        if random.random() > 0.5:
            for enemy in self.enemies_list:
                if random.random() > 0.95:  # TODO: tune this parameter to vary difficulty.
                    bullet = Bullet(initial_x=enemy.xcor(), initial_y=enemy.ycor())
                    bullet.setheading(-90)
                    self.bullets.append(bullet)

    def clean_bullets(self):  # TODO: refactor the code so you don't have to write code
        # to handle enemy bullets when there's already code to handle player bullets
        for bullet in self.bullets[-1:-1]:
            if bullet.ycor() <= SCREEN_HEIGHT / 2:
                return
            # Now we clean up the bullets out of bounds.
            bullet.hideturtle()
            self.bullets.pop()

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.forward(50)


class CollisionDetector:  # TODO: fix it so the parameters are right. The collision detection as it stands is shit.
    def __init__(self, player: Player, enemies: Enemies):
        self.associated_player = player
        self.associated_enemies = enemies

    def naive_collision_detection(self):
        # TODO: optimize this garbage
        for bullet in self.associated_player.bullets:
            for enemy in self.associated_enemies.enemies_list:
                if (0 <= abs(bullet.ycor() - enemy.ycor()) <= 10) and (0 <= abs(bullet.xcor() - enemy.xcor()) <= 10):
                    self.associated_enemies.kill(enemy)
        for bullet in self.associated_enemies.bullets:
            if (0 <= abs(bullet.ycor() - self.associated_player.ycor()) <= 10) and \
                    (0 <= abs(bullet.xcor() - self.associated_player.xcor()) <= 10):
                print("GAME OVER")

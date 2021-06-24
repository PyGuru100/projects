from classes_and_constants import Player, SCREEN_WIDTH, SCREEN_HEIGHT, Enemies, CollisionDetector
from turtle import Screen
from time import sleep

screen = Screen()
screen.tracer(0)
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
player = Player(initial_x=0, initial_y=(-SCREEN_HEIGHT/2 + SCREEN_HEIGHT/10))
enemies = Enemies()
collision_detector = CollisionDetector(player=player, enemies=enemies)

# The controls:
screen.listen()


def cannon_left():
    if player.cannon.heading() >= 130:
        return
    player.cannon.setheading(player.cannon.heading() + 10)


def cannon_right():
    if player.cannon.heading() <= 50:
        return
    player.cannon.setheading(player.cannon.heading() - 10)


def w():
    player.shoot()


def player_right():
    if player.xcor() > (SCREEN_WIDTH/2 - SCREEN_WIDTH/10):
        return
    player.move_player('right')


def player_left():
    if player.xcor() < (-SCREEN_WIDTH/2 + SCREEN_WIDTH/10):
        return
    player.move_player('left')


screen.onkeypress(fun=cannon_left, key='Left')
screen.onkeypress(fun=cannon_right, key='Right')
screen.onkeypress(fun=player_right, key='d')
screen.onkeypress(fun=player_left, key='a')
screen.onkeypress(fun=w, key='w')


while True:
    player.move_bullets()
    enemies.move()
    enemies.shoot()
    enemies.move_bullets()
    collision_detector.naive_collision_detection()
    sleep(0.1)
    screen.update()

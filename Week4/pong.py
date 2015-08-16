# Implementation of classic arcade game Pong

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20 
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = [HALF_PAD_WIDTH, HEIGHT/2]
paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT/2]
paddle1_vel = 0 
paddle2_vel = 0
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0, 0]
score1 = 0 
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    if (direction == RIGHT):
        ball_vel[0] = random.randrange(2, 4)
        ball_vel[1] = -random.randrange(1, 3)
    else:
        ball_vel[0] = -random.randrange(2, 4)
        ball_vel[1] = -random.randrange(1, 3)

def spawn_paddle():
    global paddle1_pos, paddle2_pos
    paddle1_pos = [HALF_PAD_WIDTH, HEIGHT/2]
    paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT/2]
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    dir = random.randrange(0, 2)
    score1 = 0
    score2 = 0
    if (dir == 0):
        spawn_ball(LEFT)
    else:
        spawn_ball(RIGHT)
    spawn_paddle()

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]
    
    # Bounce off the top and bottom walls
    if (ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
    
    # Reflect if ball hits paddle, else spawn a new ball.
    if (ball_pos[0] <= BALL_RADIUS + PAD_WIDTH):
        if (abs(ball_pos[1] - paddle1_pos[1]) < HALF_PAD_HEIGHT):
            ball_vel[0] = -1.1*ball_vel[0]
            ball_vel[1] = 1.1*ball_vel[1]            
        else:
            score2 = score2 + 1
            spawn_ball(RIGHT)
        
    if (ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS):
        if (abs(ball_pos[1] - paddle2_pos[1]) < HALF_PAD_HEIGHT):
            ball_vel[0] = -1.1*ball_vel[0]
            ball_vel[1] = 1.1*ball_vel[1]            
        else:
            score1 = score1 + 1
            spawn_ball(LEFT)
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'Red', 'White')
    
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos[1] + paddle1_vel >= HALF_PAD_HEIGHT and paddle1_pos[1] + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT):
        paddle1_pos[1] = paddle1_pos[1] + paddle1_vel
    else:
        if (paddle1_pos[1] <= HEIGHT/2):
            paddle1_pos[1] = HALF_PAD_HEIGHT
        else:
            paddle1_pos[1] = HEIGHT - HALF_PAD_HEIGHT
    
    if (paddle2_pos[1] + paddle2_vel >= HALF_PAD_HEIGHT and paddle2_pos[1] + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT):
        paddle2_pos[1] = paddle2_pos[1] + paddle2_vel
    else:
        if (paddle2_pos[1] <= HEIGHT/2):
            paddle2_pos[1] = HALF_PAD_HEIGHT
        else:
            paddle2_pos[1] = HEIGHT - HALF_PAD_HEIGHT
    
    # draw paddles
    canvas.draw_polygon([(0, paddle1_pos[1] - HALF_PAD_HEIGHT), (paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT), (paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT), (0,paddle1_pos[1] + HALF_PAD_HEIGHT)], 1, 'Green', 'Green')
    canvas.draw_polygon([(paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT), (paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT), (paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT), (paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT)], 1, 'Green', 'Green')
    
    # draw scores
    canvas.draw_text(str(score1), (WIDTH/4 - 7, 50), 40, "White")
    canvas.draw_text(str(score2), (3*WIDTH/4 - 7, 50), 40, "White") 
    
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if(key == simplegui.KEY_MAP["w"]):
        paddle1_vel = -5
    if(key == simplegui.KEY_MAP["s"]):
        paddle1_vel = 5
    if(key == simplegui.KEY_MAP["up"]):
        paddle2_vel = -5
    if(key == simplegui.KEY_MAP["down"]):
        paddle2_vel = 5
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    # The 'and paddle_vel ==' is added because - If 'up' is pressed and before releasing it,
    # 'down' is pressed, the paddle moves downwards(Thats fine). After that if 'up' is released,
    # the paddle stops it downward motion, if 'up' is released. This creates a problem
    # while reversing the direction of the paddle in a hurry.
    if(key == simplegui.KEY_MAP["w"] and paddle1_vel == -5):
        paddle1_vel = 0
    if(key == simplegui.KEY_MAP["s"] and paddle1_vel == 5):
        paddle1_vel = 0
    if(key == simplegui.KEY_MAP["up"] and paddle2_vel == -5):
        paddle2_vel = 0
    if(key == simplegui.KEY_MAP["down"] and paddle2_vel == 5):
        paddle2_vel = 0

def restart():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', restart, 100)


# start frame
new_game()
frame.start()

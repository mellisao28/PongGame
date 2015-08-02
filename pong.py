# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2


# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos=[WIDTH/2,HEIGHT/2]
    if (right == True):
        ball_vel=[random.randrange(120, 240)/60,-random.randrange(60, 180)/60]
    else:
        ball_vel=[-random.randrange(120, 240)/60,-random.randrange(60, 180)/60]
    pass

# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    paddle1_pos= [PAD_WIDTH-HALF_PAD_WIDTH, (HEIGHT/2)-HALF_PAD_HEIGHT]
    paddle2_pos= [WIDTH-HALF_PAD_WIDTH, (HEIGHT/2)-HALF_PAD_HEIGHT]
    paddle1_vel= [0,0] 
    paddle2_vel= [0,0]
    score1 = 0
    score2 = 0
    ball_init(True)
    pass

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # update paddle's vertical position, keep paddle on the screen
    
    paddle1_pos[1]+=paddle1_vel[1]
    paddle2_pos[1]+=paddle2_vel[1]
    
    # Keep paddle left on the screen
    if paddle1_pos[1]<=0:
        paddle1_pos[1]=0
    elif paddle1_pos[1]+PAD_HEIGHT >= HEIGHT:    
        paddle1_pos[1]=HEIGHT-PAD_HEIGHT
    
    # Keep paddle right on the screen
    if paddle2_pos[1]<=0:
        paddle2_pos[1]=0
    elif paddle2_pos[1]+PAD_HEIGHT >= HEIGHT:    
        paddle2_pos[1]=HEIGHT-PAD_HEIGHT
       
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    c.draw_line(paddle1_pos,[paddle1_pos[0],paddle1_pos[1] + PAD_HEIGHT], PAD_WIDTH, 

"White")
    c.draw_line(paddle2_pos,[paddle2_pos[0],paddle2_pos[1] + PAD_HEIGHT], PAD_WIDTH, 

"White")
    
    # update ball
    # bounce when touching top or bottom
    if (ball_pos[1]-(BALL_RADIUS+1) <= 0) or(ball_pos[1]+BALL_RADIUS+1 >= HEIGHT):
        ball_vel[1]=-ball_vel[1]
        
    # bounce when touching paddles left or right    
    elif (ball_pos[0]-(BALL_RADIUS+1) <= paddle1_pos[0]+HALF_PAD_WIDTH and ball_pos

[1]>=paddle1_pos[1] and ball_pos[1]<=paddle1_pos[1] + PAD_HEIGHT):
        ball_vel[0]=-ball_vel[0]*1.1
    elif (ball_pos[0]+(BALL_RADIUS+1) >= paddle2_pos[0]-HALF_PAD_WIDTH and ball_pos

[1]>=paddle2_pos[1] and ball_pos[1]<=paddle2_pos[1] + PAD_HEIGHT):
        ball_vel[0]=-ball_vel[0]*1.1
        
    # re-init ball when touching gutters
    elif (ball_pos[0]-(BALL_RADIUS+1) <= PAD_WIDTH):
        score2+=1
        ball_init(True)
    elif ball_pos[0]+(BALL_RADIUS+1) >= WIDTH-PAD_WIDTH:  
        score1+=1
        ball_init(False)
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 12, "Green", "White")
    c.draw_text(str(score1), (WIDTH/2-70, 80), 50, "White")
    c.draw_text(str(score2), (WIDTH/2+40, 80), 50, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 5
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = 5
    
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = -5
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = -5
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 0
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = 0
    
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = 0
    elif key==simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", init, 100)


# start frame
init()
frame.start()


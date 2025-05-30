import turtle  # import turtle module for graphics
import random  # import random module to randomize brick colors
import os
import sys
import time 


# --- Constants ---
SCREEN_WIDTH = 800  # width of the game screen
SCREEN_HEIGHT = 600  # height of the game screen
BRICK_COLORS = ["red", "orange", "green", "yellow", "pink"]  # list of colors for bricks

# ******************* Supporting Functions & Classes ******************* 
# --- Paddle Class --- 
class Paddle(turtle.Turtle):
    def __init__(self):
        """Initialize the paddle with specified shape, color, and position."""
        super().__init__()  # call parent Turtle class constructor
        self.shape("square")  # set the paddle shape to square
        self.color("white")  # set the paddle color to white
        self.shapesize(stretch_wid=1, stretch_len=5)  # stretch the paddle to make it wider
        self.penup()  # prevent drawing lines when the paddle moves
        self.goto(0, -250)  # set the paddle's initial position near the bottom center

    def move_left(self):
        """Move the paddle left within the screen boundaries."""
        x = self.xcor()  # get the current x-coordinate of the paddle
        if x > -SCREEN_WIDTH // 2 + 50:  # check if the paddle is not too far left
            self.setx(x - 40)  # move the paddle 40 units left

    def move_right(self):
        """Move the paddle right within the screen boundaries."""
        x = self.xcor()  # get the current x-coordinate of the paddle
        if x < SCREEN_WIDTH // 2 - 50:  # check if the paddle is not too far right
            self.setx(x + 40)  # move the paddle 40 units right

# --- Ball Class ---
class Ball(turtle.Turtle):
    def __init__(self):
        """Initialize the ball with starting position and movement speeds."""
        super().__init__()  # call parent Turtle class constructor
        self.shape("circle")  # set the ball shape to circle
        self.color("red")  # set the ball color to red
        self.penup()  # prevent drawing lines when the ball moves
        self.goto(0, -200)  # set the ball's initial position
        self.dx = 3  # horizontal speed
        self.dy = 3  # vertical speed

    def move(self):
        """Move the ball by updating its position based on current speed."""
        self.setx(self.xcor() + self.dx)  # update the x-coordinate
        self.sety(self.ycor() + self.dy)  # update the y-coordinate

    def bounce_x(self):
        """Reverse the horizontal movement direction of the ball."""
        self.dx *= -1  # invert the horizontal speed

    def bounce_y(self):
        """Reverse the vertical movement direction of the ball."""
        self.dy *= -1  # invert the vertical speed

    def reset_position(self):
        """Reset the ball to the center and reverse vertical direction."""
        self.goto(0, -200)  # reset ball position
        self.bounce_y()  # reverse the vertical direction

# --- Brick Class ---
class Brick(turtle.Turtle):
    """Brick object that can be broken"""
    def __init__(self, position, color):
        super().__init__()
        self.shape("square")
        self.color(color)
        self.shapesize(stretch_wid=1, stretch_len=3)
        self.penup()
        self.goto(position)

# --- Brick Class ---
class Brick(turtle.Turtle):
    def __init__(self, position, color):
        """Initialize a brick with given position and color."""
        super().__init__()  # call parent Turtle class constructor
        self.shape("square")  # set brick shape to square
        self.color(color)  # assign color to brick
        self.shapesize(stretch_wid=1, stretch_len=3)  # set brick size
        self.penup()  # prevent drawing
        self.goto(position)  # set brick's position

# --- Scoreboard Class ---
class Scoreboard(turtle.Turtle):
    def __init__(self):
        """Initialize the scoreboard with score and lives."""
        super().__init__()  # call parent Turtle class constructor
        self.score = 0  # initialize score
        self.lives = 3  # initialize lives
        self.color("white")  # set text color
        self.penup()  # prevent drawing
        self.hideturtle()  # hide turtle cursor
        self.goto(0, 260)  # position text at top center
        self.update_display()  # display initial score and lives

    def update_display(self):
        """Update the scoreboard text with current score and lives."""
        self.clear()  # clear previous scoreboard text
        self.write(f"Score: {self.score}   Lives: {self.lives}", align="center", font=("Courier", 18, "normal"))  # draw updated text

    def increase_score(self):
        """Increase the score by one and update the display."""
        self.score += 1  # increment score
        self.update_display()  # refresh scoreboard

    def lose_life(self):
        """Decrease the number of lives by one and update the display."""
        self.lives -= 1  # decrease lives
        self.update_display()  # refresh scoreboard

    def game_over(self):
        """Display 'GAME OVER' message on the screen."""
        self.goto(0, 0)  # Move to screen center
        self.write("GAME OVER", align="center", font=("Courier", 24, "bold"))  # display game over text

# --- Restart Button ---
restart_button = turtle.Turtle()  # create turtle for restart button
restart_button.hideturtle()  # hide the restart button initially

def show_restart_button():
    """Display the clickable restart button on the screen."""
    restart_button.clear()  # clear any previous text
    restart_button.penup()  # prevent drawing
    restart_button.color("white")  # set color to white
    restart_button.goto(0, -30)  # position below center
    restart_button.write("Click Here to Restart", align="center", font=("Courier", 16, "normal"))  # display button text
    restart_button.showturtle()  # show the restart button
    turtle.onscreenclick(check_restart_click)  # bind click event

def hide_restart_button():
    """Remove the restart button and disable click event."""
    restart_button.clear()  # clear the text
    restart_button.hideturtle()  # hide the turtle
    turtle.onscreenclick(None)  # disable click event

def check_restart_click(x, y):
    if -150 < x < 150 and -50 < y < 0:
        turtle.bye()  # close turtle window
        os.execv(sys.executable, ['python'] + sys.argv)  # relaunch the script

# ******************* Main Game Function *******************
# --- Game Logic ---
def run_game():
    """Initialize and run the breakout game session."""
    #win.clear()  # clear the screen
    win.reset()
    win.bgcolor("black")  # set background color
    win.tracer(0)  # disable auto-refresh

    paddle = Paddle()  # create paddle
    ball = Ball()  # create ball
    scoreboard = Scoreboard()  # create scoreboard

    bricks = []  # list to store bricks
    for y in range(250, 150, -25):  # rows of bricks
        for x in range(-350, 400, 75):  # columns of bricks
            brick = Brick((x, y), random.choice(BRICK_COLORS))  # create brick
            bricks.append(brick)  # add brick to list

    # start the game
    win.listen()  # listen for key events
    win.onkeypress(paddle.move_left, "Left")  # bind left arrow
    win.onkeypress(paddle.move_right, "Right")  # bind right arrow

    # make sure when user manually close the window, the while loop exit instead of updating the GUI after the canvas is destroyed
    try:
        while True:
            win.update()  # update screen
            ball.move()  # move the ball
            time.sleep(0.01) # count for the issue the turtle library update the GUI too fast and the ball looks like going through the bricks 

            # ball bounce conditions 
            if ball.xcor() > 390 or ball.xcor() < -390:  # check side walls
                ball.bounce_x()  # reverse horizontal direction
            if ball.ycor() > 290:  # check top wall
                ball.bounce_y()  # reverse vertical direction
            
            # game lose conditions 
            if ball.ycor() < -290:  # check bottom miss
                scoreboard.lose_life()  # decrease life
                ball.reset_position()  # reset ball
                if scoreboard.lives == 0:  # game over condition
                    scoreboard.game_over()  # display message
                    show_restart_button()  # show restart option
                    break  # exit loop

            if (ball.ycor() < -240 and ball.ycor() > -250) and \
            (paddle.xcor() - 50 < ball.xcor() < paddle.xcor() + 50):  # paddle hit check
                ball.sety(-240)  # adjust ball position
                ball.bounce_y()  # reverse direction

            # count for the issue that the ball hit the brick but it is not hide immediately and the ball looks like hit an invisible brick
            for brick in bricks[:]:  # loop over a copy of the list to allow safe modification
                if isinstance(brick, Brick) and brick.isvisible() and ball.distance(brick) < 25:
                    brick.hideturtle()  # hide the brick immediately
                    bricks.remove(brick)  # remove the brick from the list
                    ball.bounce_y()  # bounce the ball
                    scoreboard.increase_score()  # update the score

                    # win condition
                    if len(bricks) == 0:  # remove all the bricks
                        win_message = turtle.Turtle()  # create message
                        win_message.hideturtle()  # hide cursor
                        win_message.color("white")  # set text color
                        win_message.penup()  # prevent drawing
                        win_message.goto(0, 0)  # center position
                        win_message.write("YOU WIN!", align="center", font=("Courier", 24, "bold"))  # display win text
                        show_restart_button()  # show restart option
                        return  # end game
                    break  # exit brick loop
    except (turtle.Terminator, Exception): # counted for the error message when user close the window manually but the loop continues
        pass 

# --- Screen Setup ---
win = turtle.Screen()  # create game screen
win.title("Breakout Game with Restart")  # set window title
win.bgcolor("black")  # set background color
win.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)  # set screen size

# --- Main Entry Function ---
def main():
    """Main function to start the game."""
    run_game()  # start game session
    win.mainloop()  # keep window open

# --- Entry Point ---
if __name__ == '__main__':
    main()  # launch the main function
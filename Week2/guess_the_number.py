# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import math

# declare global variables
low = 0
high = 100
secret_number = 0
num_guesses = 0

# helper function to start and restart the game
def new_game():
    global low, high, secret_number, num_guesses
    print "New Game. Range is from", low, "to",high
    num_guesses = int(math.ceil(math.log(high, 2)))
    print "Number of remaining guesses is", num_guesses, "\n"
    secret_number = random.randrange(low, high)
    return

# define event handlers for control panel
def range100():
    global low, high
    low = 0
    high = 100
    new_game()
    return 

def range1000():
    global low, high
    low = 0
    high = 1000
    new_game()
    return 
    
def input_guess(guess):
    global num_guesses
    num_guesses = num_guesses - 1
    int_guess = int(guess)
    print "Guess was", guess
    print "Number of remaining guesses is", num_guesses

    if(secret_number < int_guess):
        if(num_guesses > 0):
            print "Lower!\n"
        else:
            print "You ran out of guesses. The number was", secret_number, "\n"
            new_game()
    elif(secret_number > int_guess):
        if(num_guesses > 0):
            print "Higher!\n"
        else:
            print "You ran out of guesses. The number was", secret_number, "\n"
            new_game()
    else:
        print "Correct!\n"
        new_game()
    return
    
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range is [0, 100)", range100, 200)
frame.add_button("Range is [0, 1000]", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)

# call new_game 
new_game()
frame.start()

# always remember to check your completed program against the grading rubric

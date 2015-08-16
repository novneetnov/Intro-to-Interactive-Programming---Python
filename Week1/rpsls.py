# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random

# helper functions

def name_to_number(name):
    num = 0
    if(name == 'rock'):
        num = 0
    elif(name == 'Spock'):
        num = 1
    elif(name == 'paper'):
        num = 2
    elif(name == 'lizard'):
        num = 3
    elif(name == 'scissors'):
        num = 4
    else:
        num = None
    return num

def number_to_name(number):
    name = ''
    if(number == 0):
        name = 'rock'
    elif(number == 1):
        name = 'Spock'
    elif(number == 2):
        name = 'paper'
    elif(number == 3):
        name = 'lizard'
    elif(number == 4):
        name = 'scissors'
    else:
        name = None
    return name
    

def rpsls(player_choice):
    
    print "\n"

    print "Player chooses " + player_choice
    
    player_number = name_to_number(player_choice)

    comp_number = random.randrange(0,5)
    
    comp_choice = number_to_name(comp_number)
    
    print "Computer chooses " + comp_choice
    
    if (player_number != None):
        clock_anticlock = (player_number - comp_number) % 5
     
        if(clock_anticlock == 1 or clock_anticlock == 2):
            print "Player wins!"
        elif(clock_anticlock == 3 or clock_anticlock == 4):
            print "Computer wins!"
        else:
            print "Player and computer tie!"
    
    else:
        print "Bad Player Choice! Choose wisely!"
    
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
rpsls("sciddssors")
# always remember to check your completed program against the grading rubric



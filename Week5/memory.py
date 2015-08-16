# implementation of card game - Memory

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# helper function to initialize globals
def new_game():
    global num_list, exposed, state, turns
    num_list = range(0,8)
    num_list.extend(num_list)
    random.shuffle(num_list) 
    exposed = []
    state = 0
    turns = 0
    label.set_text("Turns = "+str(turns))
     
# define event handlers
def mouseclick(pos):
    global state, turns
    card_num = pos[0]/50
    if card_num not in exposed:
        if state == 1:
            exposed.append(card_num)
            if num_list[exposed[-1]] == num_list[exposed[-2]]:
                state = 0
            else:
                state = 2
        elif state == 2:
            exposed.pop(-1)
            exposed.pop(-1)
            exposed.append(card_num)
            state = 1
            turns = turns + 1
        else:
            exposed.append(card_num)
            state = 1
            turns = turns + 1
    label.set_text("Turns = "+str(turns))
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    count = 0
    for num in num_list:
        canvas.draw_text(str(num), (50*count+17, 65), 40, 'White')
        if count not in exposed:
            canvas.draw_polygon([[50*count, 0], [50*(count+1), 0], [50*(count+1), 100], [50*count, 100]], 2, 'Red', 'Green')
        count = count + 1

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric
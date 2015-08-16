# template for "Stopwatch: The Game"
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


# define global variables
tenths = 0
stopwatch_time = "0:00.0"
timer_running = False
total_stops = 0
successful_stops = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    tenth = t % 10
    sec_unit = (t/10) % 10
    sec_tens = (t/100) % 6
    mins = t/600
    return str(mins)+":"+str(sec_tens)+str(sec_unit)+"."+str(tenth)

# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    global timer_running
    timer.start()
    timer_running = True

def stop_handler():
    timer.stop()
    global total_stops, successful_stops, timer_running, tenths
    if(timer_running):
        total_stops = total_stops + 1
        timer_running = False
        if(tenths % 10 == 0):
            successful_stops = successful_stops + 1

def reset_handler():
    timer.stop()
    global tenths, stopwatch_time, total_stops, successful_stops, timer_running
    tenths = 0
    stopwatch_time = "0:00.0"
    total_stops = 0
    successful_stops = 0
    timer_running = False
    
# define event handler for timer with 0.1 sec interval
def timer_handler():
    global tenths, stopwatch_time
    tenths = tenths + 1
    stopwatch_time = format(tenths)

# define draw handler
def draw_handler(canvas):
    global tenths
    canvas.draw_text(stopwatch_time, (50,110), 45, "Red")
    canvas.draw_text(str(successful_stops)+"/"+str(total_stops), (155,25), 20, "Green")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 200, 200)

# register event handlers
frame.add_button("Start", start_handler, 80)
frame.add_button("Stop", stop_handler, 80)
frame.add_button("Reset", reset_handler, 80)
frame.set_draw_handler(draw_handler)
timer = simplegui.create_timer(100, timer_handler)

# start frame
frame.start()
# Please remember to review the grading rubric

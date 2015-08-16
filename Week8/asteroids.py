# program template for Spaceship
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False
FRICTION_COEFF = 0.01
ANGULAR_VEL_SHIP = 3.14/50
ACC_SHIP = 0.1 
ANGULAR_VEL_ROCK = 3.14/60

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue2.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
    
    def shoot(self):
        global missile_group
        missile_pos = [0,0]
        missile_pos[0] =  self.pos[0] + self.radius*math.cos(self.angle)
        missile_pos[1] =  self.pos[1] + self.radius*math.sin(self.angle)
        missile_vel = [0,0]
        missile_vel[0] = self.vel[0] + 6*math.cos(self.angle)
        missile_vel[1] = self.vel[1] + 6*math.sin(self.angle)
        missile_group.add(Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound))
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def setThrust(self, thrust):
        self.thrust = thrust
    
    def getThrust(self):
        return self.thrust
    
    def setAngVel(self, angle_vel):
        self.angle_vel = angle_vel
        
    def getAngVel(self):
        return self.angle_vel
    
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)   
            ship_thrust_sound.play()
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            ship_thrust_sound.rewind()
            
    def update(self):
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # update angle
        self.angle += self.angle_vel
        
        # update velocity
        if self.thrust:
            self.vel[0] += ACC_SHIP*angle_to_vector(self.angle)[0]
            self.vel[1] += ACC_SHIP*angle_to_vector(self.angle)[1]
        
        self.vel[0] = (1 - FRICTION_COEFF)*self.vel[0]
        self.vel[1] = (1 - FRICTION_COEFF)*self.vel[1]
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other_obj):
        collision = False
        distance = dist(self.get_position(), other_obj.get_position())
        if distance <= self.get_radius() + other_obj.get_radius():
            collision = True
        return collision
            
    def draw(self, canvas):
        if self.animated:
            explosion_center = self.image_center
            canvas.draw_image(self.image, 
                              [explosion_center[0] + self.age*self.image_size[0], 
                               explosion_center[1]],
                               self.image_size, self.pos, self.image_size)
        else :
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # update angle
        self.angle += self.angle_vel
        
        # update age of the Sprite
        self.age += 1   
        if self.age >= self.lifespan:
            return True
        return False

# draw_handler        
def draw(canvas):
    global time, lives, score, started, rock_group, missile_group, explosion_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and update it
    my_ship.draw(canvas)
    my_ship.update()
    
    # detect collision of rocks and ship and update lives
    collision = group_collide(rock_group, my_ship)
    if collision:
        lives -= 1
        if lives == 0:
             reset_params()
    
    # Detect collisions between rocks and missiles
    num_collisions = group_group_collide(rock_group, missile_group)
    score += num_collisions*10
    
    # draw and update the rock_group, missile_group and explosion_group
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # draw score and lives
    canvas.draw_text("Lives", [50,50], 30, "White")
    canvas.draw_text(str(lives), [50,80], 30, "White")
    canvas.draw_text("Score", [WIDTH - 120,50], 30, "White")
    canvas.draw_text(str(score), [WIDTH - 120,80], 30, "White")
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(),
                          [WIDTH / 2, HEIGHT / 2], splash_info.get_size()) 

# reset parameters
def reset_params():
    global started, rock_group, my_ship, cont_shoot_timer
    started = False
    rock_group = set([])
    soundtrack.rewind()
    my_ship.setAngVel(0)
    my_ship.setThrust(False)
    cont_shoot_timer.stop()
    
# helper function to detect group collisions of Sprite_group and Missile_group
def group_group_collide(rock_group, missile_group):
    num_collisions = 0
    for rock in list(rock_group):
        if group_collide(missile_group, rock):
            rock_group.remove(rock)
            num_collisions += 1
    return num_collisions
        
# helper function to detect group collisions of Sprite and the ship
def group_collide(group, other_obj):
    collision = False
    for sprite_obj in list(group):
        if sprite_obj.collide(other_obj):
            group.remove(sprite_obj)
            collision = True
            add_explosion_group([(sprite_obj.get_position()[0]+other_obj.get_position()[0])/2,
                                (sprite_obj.get_position()[1]+other_obj.get_position()[1])/2])
    return collision

# helper function to create and add explosion object(instance of Sprite Class)
def add_explosion_group(explosion_pos):
    global explosion_group
    explosion_sprite = Sprite(explosion_pos, [0, 0], 
                            0, 0, explosion_image, explosion_info, explosion_sound)
    explosion_group.add(explosion_sprite)
    
# helper function to draw and update the rock_group and missile_group       
def process_sprite_group(sprite_group, canvas):
    for sprite in list(sprite_group):
        sprite.draw(canvas)
        check_remove = sprite.update()
        if check_remove:
            sprite_group.remove(sprite)

# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, started, my_ship, score
    if started:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        
        # Adaptive rock velocity - Higher the score, more difficult the game
        rock_vel = [0,0]
        if score < 50:
            rock_vel = [random.randrange(-5,5)/5.0,random.randrange(-5,5)/5.0]
        elif score < 150:
            rock_vel = [random.randrange(-10,10)/5.0,random.randrange(-10,10)/5.0]
        elif score < 250:
            rock_vel = [random.randrange(-15,15)/5.0,random.randrange(-15,15)/5.0]
        elif score < 350:
            rock_vel = [random.randrange(-20,20)/5.0,random.randrange(-20,20)/5.0]
        else:
            rock_vel = [random.randrange(-25,25)/5.0,random.randrange(-25,25)/5.0]
        
        # Prevent spawning rocks too close to the ship.
        ship_dist = dist(rock_pos, my_ship.get_position())
        if len(rock_group) < 12 and ship_dist >= 5*my_ship.get_radius():
            rock_group.add(Sprite(rock_pos, rock_vel, 
                            0, ANGULAR_VEL_ROCK, asteroid_image, asteroid_info))
    
# key handlers to control ship
def keydown(key):
    global started, cont_shoot_timer
    if started:
        if key == simplegui.KEY_MAP['left']:
            my_ship.setAngVel(-ANGULAR_VEL_SHIP)
        if key == simplegui.KEY_MAP['right']:
            my_ship.setAngVel(ANGULAR_VEL_SHIP)
        if key == simplegui.KEY_MAP['up']:
            my_ship.setThrust(True)
        if key == simplegui.KEY_MAP['space']:
            my_ship.shoot()
            cont_shoot_timer.start()

def keyup(key):
    global cont_shoot_timer
    if key == simplegui.KEY_MAP['left'] and my_ship.getAngVel() == -ANGULAR_VEL_SHIP:
        my_ship.setAngVel(-0)
    if key == simplegui.KEY_MAP['right'] and my_ship.getAngVel() == ANGULAR_VEL_SHIP:
        my_ship.setAngVel(0)
    if key == simplegui.KEY_MAP['up']:
        my_ship.setThrust(False)
    if key == simplegui.KEY_MAP['space']:
        cont_shoot_timer.stop()

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        soundtrack.play()

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)
cont_shoot_timer = simplegui.create_timer(300, my_ship.shoot)

# get things rolling
timer.start()
frame.start()

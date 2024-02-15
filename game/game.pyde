# IMPORTING REQUIRED LIBRARIES
import os
import random
import time
add_library('minim') # PROCESSING SOUND LIBRARY

sound = Minim(this)

# GLOBAL CONSTANTS

X_RES = 1400
Y_RES = 1000

TORCH_SPEED = 20
ALIEN_SPEED = 1
BULLET_SPEED = 16

path = os.getcwd()

# LOADING REQUIRED FILES INCLUDING IMAGES AND SOUNDS

ALIENS = {'ZORAX': [loadImage(path + '/images/' + 'zorax1.png'), loadImage(path + '/images/' + 'zorax2.png')],
          'LYRA': [loadImage(path + '/images/' + 'lyra1.png'), loadImage(path + '/images/' + 'lyra2.png')],
          'RIGEL': [loadImage(path + '/images/' + 'rigel1.png'), loadImage(path + '/images/' + 'rigel2.png')]}

TORCH = loadImage(path + '/images/' + 'torch.png')
SPACESHIP = loadImage(path + '/images/' + 'spaceship.png')
STARTSCREEN = loadImage(path + '/images/' + 'startscreen.png')
ENDSCREEN = loadImage(path + '/images/' + 'endscreen.png')
TORCH_BULLET = loadImage(path + '/images/' + 'laser.png')
BULLET = loadImage(path + '/images/' + 'bullet.png')
BACKGROUND = loadImage(path + '/images/' + 'background1.png')
POWERUPS = [loadImage(path + '/images/' + 'powerup_speed.png'), loadImage(path + '/images/' + 'powerup_torch.png'), loadImage(path + '/images/' + 'life.png')]
MAINMUSIC = path + '/sounds/' + 'mainloop.wav'
DAMAGE = path + '/sounds/' + 'damage.wav'
POWERUPSOUND = path + '/sounds/' + 'powerup.wav'
DEFEAT = path + '/sounds/' + 'defeat.wav'
FIRE = path + '/sounds/' + 'fire.wav'

# TORCH CLASS

class Torch:

    def __init__(self, sprite, px, py, speed, torch=False):
        self.sprite, self.px, self.py, self.speed, self.torch = sprite, px, py, speed, torch
    
    # ONLY DISPLAY THE BULLET IF IT IS SUPPOSED TO BE MOVING

    def display(self):
        if self.torch:
            image(self.sprite[1], self.px, self.py)
            self.px1 = self.px + self.sprite[1].width
            self.py1 = self.py + self.sprite[1].height
        else:
            image(self.sprite[0], self.px, self.py)
            self.px1 = self.px + self.sprite[0].width
            self.py1 = self.py + self.sprite[0].height

# BULLET CLASS FOR TORCH

class BulletTorch:

    def __init__(self, sprite, px, py, speed, moving=False):
        self.sprite, self.px, self.py, self.speed, self.px1, self.py1, self.moving = sprite, px, py, speed, px + 27, py + 43, moving

    def display_fire(self):
        if self.moving:
            self.py -= self.speed
            image(self.sprite, self.px, self.py)

    def reset(self, x, y, val):
        if val:
            self.px = x + 25
        else:
            self.px = x + 60
        self.py = y
        self.moving = False

# BULLET CLASS FOR THE INVADERS

class BulletInvader(BulletTorch):
    
    def __init__(self, sprite, px, py, speed, moving=False):
        self.sprite, self.px, self.py, self.speed, self.px1, self.py1, self.moving = sprite, px, py, -speed, px + 35, py + 55, moving

    
    def reset(self, x = -200, y = -200):
        self.px = x + 10
        self.py = y
        self.moving = False
    
    def update(self, x, y):
        self.px, self.py = x, y

# INVADER CLASS FOR ALL ALIEN CRAETURES, TWO SPRITES TO REPRESENT MOVEMENT

class Invader:

    def __init__(self, images, px, py, speed, state=0):
        self.images, self.px, self.py, self.speed, self.state, self.px1, self.py1 = images, px, py, speed, state, px + \
                                                                                                                  images[
                                                                                                                      0].width, py + \
                                                                                                                  images[
                                                                                                                      0].height
    # DISPLAYING THE INVADER OBJECT

    def display(self):
        image(self.images[self.state], self.px, self.py)
    
    # TO MOVE ALIENS IN Y AND X AND KEEP TRACK OF THEIR COORDINATES (TOP LEFT AND BOT RIGHT) FOR COLLISION DETECTION

    def shift(self, dx, dy):
        self.px += dx
        self.py += dy
        self.px1 += dx
        self.py1 += dy

# POWERUP CLASS INCLUDING ALL POWERUP OBJECTS

class Powerup:

    def __init__(self, images, px, py, px1, py1, state):
        self.images, self.px, self.py, self.px1, self.py1, self.state, self.powertime = images, px, py, px1, py1, state, time.time()
        self.keepdrawing = False
    
    # MULTIPLE STATES OF THE POWERUP OBJECT REPRESENT DIFFERENT COLLECTIBLE POWERUPS

    def powering(self):
        if time.time() - self.powertime >= 7:
            if not self.keepdrawing:
                self.choice = random.randint(0, len(POWERUPS))
                self.state = self.choice
                self.px = random.randint(200, X_RES - 300)
                self.py = random.randint(300, 600)
                self.px1 = self.px + 115
                self.py1 = self.px + 130
                self.duration = time.time()
                self.keepdrawing = True
            if self.choice == 0:
                spawn_speed = image(self.images[0], self.px, self.py)
                self.state = 0
            elif self.choice == 1:
                spawn_torch = image(self.images[1], self.px, self.py)
                self.state = 1
            elif self.choice == 2:
                spawn_life = image(self.images[2], self.px, self.py)
                self.state = 2
            if time.time() - self.duration >= 5:
                 self.powertime = time.time()
                 self.duration = time.time()
                 self.keepdrawing = False
            else:
                self.keepdrawing = True
            self.px1 = self.px + 115
            self.py1 = self.px + 230

    # TRIGGER THE USE OF A POWERUP

    def trigger(self):
        self.powertime = time.time()
        return self.state
    
    # RESETING THE OBJECT OUT OF DISPLAY SCREEN IF IT SHOULD NOT BE ON THE GAME BOARD

    def reset(self):
        self.px, self.py, self.px1, self.py1, self.powertime, self.state, self.keepdrawing = -200, -200, -200, -200, time.time(), -1, True

# MAIN GAME SPACE CLASS WHICH INTEGRATES ALL PRELIMINARY CLASSES AND RUNS THE GAME

class Space:
    
    # INITIALIZING THE REQUIRED VARIABLES OF THE GAME CLASS INCLUDING ALL THE ONES WHICH KEEP TRACK OF IN GAME INFORMATION

    def __init__(self):
        self.invaders = []
        self.torch = Torch([SPACESHIP, TORCH], 600, 900, TORCH_SPEED, False)
        self.bullet = BulletTorch(TORCH_BULLET, self.torch.px, self.torch.py, BULLET_SPEED)
        self.invaderbullet = BulletInvader(BULLET,-200, -200, 2)
        self.create()
        self.speed_increase = 1.0
        self.turn = -1
        self.score = 0
        self.ability = Powerup(POWERUPS, -200, -200, -200, -200, -1)
        self.torchtime = 0
        self.speedtime = 0
        self.invadertimer = 0
        self.lives = 3
        self.gamestart = True
        self.gameend = False
        
        self.bg_sound = sound.loadFile(MAINMUSIC)
        self.bg_sound.loop()
        self.fire_sound = sound.loadFile(FIRE)
        self.ability_sound = sound.loadFile(POWERUPSOUND)
        self.damage_sound = sound.loadFile(DAMAGE)
        self.defeat_sound = sound.loadFile(DEFEAT)
    
    # CREATE METHOD FOR THE GAME CLASS GENERATING A LIST OF INVADERS

    def create(self):
        y = 200
        for character in ALIENS:
            x = 350
            for characters_in_a_row in range(5):
                self.invaders.append(Invader(ALIENS[character], x, y, ALIEN_SPEED))
                x = x + 150
            y = y + 150
    
    # SHIFITNG THE TORCH USING USER INPUT WITH CONDITIONS ON BOUNDARIES AROUND THE BOARD

    def shift(self, _key):
        if _key == RIGHT and self.torch.px <= X_RES - 100:
            self.torch.px += TORCH_SPEED
        if _key == LEFT and self.torch.px >= 60:
            self.torch.px -= TORCH_SPEED
        if not self.bullet.moving:
            self.bullet.reset(self.torch.px, self.torch.py, self.torch.torch)
    
    # MOVING THE INVADERS ACROSS THE GAME SCREEN AND STOPPING THEM FROM GOING OUT OF SCREEN BY CALCULATING THE EXTREME MOST CORNER INVADER'S POSITION AND CHANGING DIRECTION
    # UPON CONTACT WITH THE SCREEN EDGE
    def move_invaders(self):
        highest = 0  # HIGHEST VALUE IN X
        lowest = 9999  # HIGHEST VALUE IN X TO THE LEFT (OR SMALLEST VALUE CLOSEST TO 0 FOR LEFT EDGE)
        highesty = 0  # HIGHEST VALUE IN Y SO CONSIDERING CLOSENESS TO THE BOTTOM OF THE SCREEN TO SET AND EDGE LIMIT TO HOW LOW ALIENS CAN GO

        for invader in self.invaders:
            if time.time() - self.speedtime <= 6:
                invader.shift(self.turn * invader.speed / 4, 0)
                self.bullet.speed = BULLET_SPEED
                self.torch.speed = TORCH_SPEED
            else:
                invader.shift(self.turn * (invader.speed), 0)
            
            # CHECKING THE LAST MOST INVADER SPRITE IN THE SELF.INVADERS LIST, HIGHEST REPRESENTS GREATEST X VALUE SO CHECKING FOR RIGHT EDGE

            if self.invaders[-1].px1 > highest:
                highest = self.invaders[-1].px1
            if invader.px1 > highest:
                highest = invader.px1
            if invader.py1 > highesty:
                highesty = invader.py1
                print(highesty)
                if highesty >= 900: # IF THE HIGHEST Y COORDINATE OF AN ALIEN IS GREATER THAN 900 PIXELS, WE RESET THE GAME SCREEN AND PLAYER LOSES A LIFE
                    for i in range(2):
                        for invader in self.invaders:
                            self.invaders.remove(invader)
                    self.create()
                    self.lives -= 1 # REDUCTION IN LIFE BECAUSE INVADER GOT TOO CLOSE TO THE SHIP
                    self.event_sound(3) # ACTIVATING THE SOUND FOR LOSS OF LIFE
                    
            if invader.px < lowest:
                lowest = invader.px
            if highest >= X_RES - 40: # IF INVADERS ARE TOO CLOSE TO THE RIGHT SIDE,  WE TURN THEM IN THE LEFT DIRETION
                self.turn = -1
                for invader in self.invaders:
                    invader.shift(-15, 50) # SHIFT THEM DOWN WHEN CHANGING DIRECTION TO BRING THEM CLOSER TO THE SHIP AND MOVE LEFT BY 15 PIXELS
                break
            elif lowest <= 40:
                self.turn = 1 # CHANGING MOVEMENT DIRECTION TO RIGHT IF THE ALIENS ARE TOO CLOSE TO THE LEFT SIDE
                for invader in self.invaders:
                    invader.shift(15, 50) # SHIFT THEM DOWN WHEN CHANGING DIRECTION AND MOVE RIGHT BY 15 PIXELS (X, Y) INPUT FORMAT
                break
        self.game_end()  # CHECKING IF THE GAME ENDS IN THE GIVEN FUNCTION
        if len(self.invaders) == 0:  # IF THE LENGTH OF INVADER LIST IS 0, I.E IF THE PLAYER ELIMINATES ALL INVADERS, A NEW WAVE OF INVADERS SPAWNS
            self.create()  # CREATING A NEW WAVE OF INVADERS
    
    # THIS METHOD MAKES THE INVADERS SHOOT BULLETS AT THE PLAYER
    def shoot_invaders(self):
        self.invaderbullet.speed = self.invaderbullet.speed * self.speed_increase # THE INVADER BULLET SPEED IS PROPORTIONAL THEIR OWN SPEED AND THE GAME'S DIFFICULTY
        if self.invadertimer >= 10:
            attacker = random.choice(self.invaders)
            self.invaderbullet.reset(attacker.px, attacker.py)
            self.invaderbullet.moving = True  # MAKE THE BULLET MOVEMENT TRUE
            self.invadertimer = 0 # RESET THE TIMER TO START COUNTING AGAIN
        self.invaderbullet.display_fire()
    
    # THIS METHOD CALCULATES THE SCORE OF THE PLAYER IN THE GAME BASED ON THE TYPE OF ALIEN KILLED
    def scoring(self, obj):
        up = 5
        mid, midc = 10, 5
        bot, botc = 15, 5
        if obj + 1 <= up:
            up -= 1
            mid = up + midc
            bot = mid + botc
            self.score += 15
        elif obj + 1 <= mid:
            midc -= 1
            mid = up + midc
            bot = mid + botc
            self.score += 10
        elif obj + 1 <= bot:
            botc -= 1
            mid -= 1
            bot = mid + botc
            self.score += 5
            
    # DISPLAY METHOD FOR THE SPACE CLASS
    def display(self):
        game.game_end()
        if self.gamestart:
            image(STARTSCREEN, 0, 0)
        elif not self.gameend:
            image(BACKGROUND, 0, 0)
            for invader in self.invaders:
                invader.display()
            if time.time() - self.torchtime >= 4:
                self.torch.torch = False
            self.torch.display()
            if self.bullet.py <= 150:
                self.bullet.reset(self.torch.px, self.torch.py, self.torch.torch)
            fill(255, 255, 0)
            textSize(48)
            text(str(self.score), 220, 75)
            text(str(self.lives), 1150, 80)
        elif self.gameend:
            image(ENDSCREEN, 0, 0)
            time.sleep(2)
    
    def game_start(self, keyCode): # START THE GAME WHEN SPACE KEY IS PRESSED
        if keyCode == 32:
            self.gamestart = False
    
    def game_restart(self, keyCode): # RESTART THE GAME WHEN SPACE IS PRESSED AND THE PLAYER IS OUT OF LIVES
        if self.gameend:
            if keyCode == 32:
                self.gameend = False
                self.lives = 3
                self.__init__()
    
    def game_end(self): # END THE GAME ONCE THE PLAYER IS OUT OF LIVES
        if self.lives <= 0:
            self.gameend = True
    
    # COLLISION DETECTION OF ANY BULLET WITH ANY OBJECT
    def bullet_collision(self):
        if self.bullet.py >= 100:
            for invader in self.invaders:
                if invader.py - 10 <= self.bullet.py <= invader.py1 + 10:
                    if invader.px - 5 <= self.bullet.px <= invader.px1 + 5:
                        print(self.invaders.index(invader))
                        self.scoring(self.invaders.index(invader))
                        self.invaders.remove(invader)
                        self.bullet.reset(self.torch.px, self.torch.py, self.torch.torch)
                        self.event_sound(1)  # PLAY SOUND FOR THE EVENT THAT TORCH BULLET HITS INVADER
                if invader.py - 10 <= self.torch.py <= invader.py1 + 10:
                    if invader.px - 5 <= self.torch.px <= invader.px1 + 5:
                        # IF AN INVADER HITS THE TORCH, RESET THE WAVE AND LOSE A LIFE
                        for i in range(2):
                            for invader in self.invaders:
                                self.invaders.remove(invader)
                        self.lives -= 1
                        self.create()
                        return self.event_sound(3)  # PLAY THE RESPECTIVE SOUND
                if self.bullet.px + 8 >= self.ability.px and self.bullet.px + 8 <= self.ability.px1 and self.bullet.py + 10 >= self.ability.py and self.bullet.py + 10 <= self.ability.py1:
                    self.abilities(self.ability.trigger())
                    self.ability.reset()
                    self.bullet.reset(self.torch.px, self.torch.py, self.torch.torch)
                    self.event_sound(2)  # SOUND FOR WHEN THE BULLET HITS A POWERUP
            if self.invaderbullet.px + 8 >= self.torch.px and self.invaderbullet.px + 8 <= self.torch.px1 and self.invaderbullet.py + 10 >= self.torch.py and self.invaderbullet.py + 10 <= self.torch.py1: 
                    self.invaderbullet.reset()
                    self.lives -= 1
                    return self.event_sound(3)  # WHEN AN INVADER BULLET HITS THE SPACESHIP
            return False
        
    # MANAGING GAME EVENT SOUNDS
    def event_sound(self, type):
        if type == 1:
            self.fire_sound.rewind()
            self.fire_sound.play()
        elif type == 2:
            self.ability_sound.rewind()
            self.ability_sound.play()
        elif type == 3:
            self.damage_sound.rewind()
            self.damage_sound.play()

    def abilities(self, number):  # THE ABILITIES METHOD TO MAKE THE REQUIRED GAME CHANGES BASED ON ABILITY CAUGHT
        if number == 0:
            self.bullet.speed = self.bullet.speed * 5
            self.torch.speed = self.torch.speed * 5
            self.speed_increase = 1.0
            self.speedtime = time.time()
        elif number == 1:
            self.torch.torch = True
            self.torchtime = time.time()
            for i in range(2):
                for invader in self.invaders:
                    self.scoring(self.invaders.index(invader))
                    self.invaders.remove(invader)
        else:
            if not self.lives == 3:
                self.lives += 1

    def power(self):  # POWERUP METHOD CALLING POWERING IN THE POWERUP CLASS
        self.ability.powering()

    def shoot(self, _key):  # SHOOTING BASED ON PLAYER INPUT
        if _key == 32:
            self.bullet.moving = True
        if self.bullet.py < 10:
            self.bullet.reset(self.torch.px, self.torch.py, self.torch.torch)
    
    def time_event(self):  # EVENTS BASED ON TIME
        for invader in self.invaders:
            invader.state = (invader.state + 1) % 2  # CHANGING ALIEN SPRITE FOR MOVEMENT ANIMATION
            invader.speed += 0.06  # INCREASING SPEED
        self.invadertimer += 1  # INVADER TIMER INCREASES EVERY HALF A SECOND


game = Space()  # GAME OBJECT


# INTERNAL TIME BASED EVENTS COUNTERS
global START_TIME
START_TIME = time.time()
global SPAWN_TIME
SPAWN_TIME = time.time()

def setup():
    size(X_RES, Y_RES)
    background(255, 255, 255)
    frameRate(180)


def draw():
    global SPAWN_TIME
    global START_TIME
    
    game.display()
    if not game.gamestart and not game.gameend:  # IF THE GAME HAS ENDED OR HAS NOT STARTED, NOT CALLING THESE FUNCTIONS
        game.bullet.display_fire()
        game.move_invaders()
        game.shoot_invaders()
        if game.bullet.moving or game.invaderbullet.moving:  # CHECK FOR COLLISION ONLY IF ONE OF THE BULLETS IS MOVING
            game.bullet_collision()
        if time.time() - START_TIME >= 0.5:
            game.time_event()
            START_TIME = time.time()
        game.power()  # CALLING THE POWER METHOD
        
# TAKING INPUT
def keyPressed():
    game.shift(keyCode)
    game.game_start(keyCode)
    game.game_restart(keyCode)

# CAN ONLY SHOOT UPON RELEASE TO NOT ABUSE THE SHOOTING ABILITY
def keyReleased():
    game.shoot(keyCode)

#! usr/bin/python
# PongClone- A Python and Pygame version of the classic arcade game.
 #   Copyright (C) 2011 T. S. Hayden Dennison
#
 #   This program is free software: you can redistribute it and/or modify
  #  it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
 #   This program is distributed in the hope that it will be useful,
 #   but WITHOUT ANY WARRANTY; without even the implied warranty of
 #   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #   GNU General Public License for more details.
#
 #   You should have received a copy of the GNU General Public License
  #  along with this program.  If not, see <http://www.gnu.org/licenses/>.
# UPDATE 01/08/2011: added two player mode, updated menu
# UPDATE 01/09/2011: updated ball physics, fixed second player and enemy having unfair adventage by being closer to the wall
# ball is now smaller, with randomized speeds when someone scores.
# UPDATE 01/11/2011: added code to stop ball from resetting its speed to 0
# UPDATE 01/19/2011: added sound effects and better menu.
import pygame, sys, time, random, os, math, copy
from pygame.locals import *

pygame.init()
size = width, height = 640, 480
screen = pygame.display.set_mode(size)
pygame.display.set_caption('PongClone')
white = [255, 255, 255]
black = [0, 0, 0]
blue = [33, 33, 192]
red = [192, 33, 33]
clock = pygame.time.Clock()

def random_color():
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

###################################################################################################################################################################
# This is a menu class module. You can make text-based menus of any length with it
# SimMen - menu class module with example
 #   Copyright (C) 2011 T. S. Hayden Dennison
#
 #   This program is free software: you can redistribute it and/or modify
  #  it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
 #   This program is distributed in the hope that it will be useful,
 #   but WITHOUT ANY WARRANTY; without even the implied warranty of
 #   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #   GNU General Public License for more details.
#
 #   You should have received a copy of the GNU General Public License
  #  along with this program.  If not, see <http://www.gnu.org/licenses/>
# UPDATE 01/14/2011: fixed window being too big.
# UPDATE 01/15/2011: added mouse control, rewrote most of the menu.update() code.
# UPDATE 01/18/2011: Fixed some syntax and run-time bugs.
# Menu.run() needs the latest event to stop it interfering with your program's event que. You DON'T have to paint over the menu, it takes care of that itself.
# Spent more time (once again) fixing that elusive "maxsize" glitch.

class Menu():
    # Menu class definition
    # need a position to init, minimum
    # Provides some limited cusomizability
    # Uses system font so it's compatible with anything
    def __init__(self, pos, data=[], textsize=32,\
            wordcolor=[255, 255, 0], backcolor=[0, 0, 255], selectedcolor=[0, 255, 255], lprn=20):
        import pygame
        self.rect = pygame.Rect((pos), (0, 0))
        self.data = data
        self.textrects = []
        self.textsurfs = []
        self.cursorpos = 0
        self.pos = pos
        self.font = pygame.font.SysFont(None, 32)
        self.wordcolor = wordcolor
        self.backcolor = backcolor
        self.selectedcolor = selectedcolor
        self.textsize = textsize
        self.looprun = lprn#looprun
        self.scroll = False
        self.selected = False
        for word in self.data:
            self.textsurfs.append(self.font.render(str(word), True, self.wordcolor))
            rect = self.font.render(str(word), True, self.wordcolor).get_rect()
            self.textrects.append(rect)
    def add(self, words):
        # add one or more elements of data
        self.data.extend(words)
        for word in words:
            self.textrects.append(self.font.render(str(word), True, self.wordcolor).get_rect())
            self.textsurfs.append(self.font.render(str(word), True, self.wordcolor))
    def remove(self, item=False):
        if not item:
            # Remove the last element of data
            self.data.pop()
            self.textrects.pop()
            self.textsurfs.pop()
        else:
            thingpop = self.data.index(item)
            self.data.pop(thingpop)
            self.textrects.pop(thingpop)
            self.textsurfs.pop(thingpop)
    def update(self, screen, event):
        import pygame
        # Blit and updated the text box, check key presses
        height = 0
        curpos = []# Stop python from making curpos and self.pos point to the same list
        for n in self.pos:
            curpos.append(n)
        curpos[0] += 1
        self.rect.height = len(self.data)*self.textsize# Define the max height of the text box
        if self.rect.height > screen.get_height():
            self.scroll = True
        else:
            self.scroll = False
        # Define the max width of the text box based on the word length it holds
        maxsize = sorted(self.data)
        maxsize = len(maxsize[0])
        self.rect.width = maxsize*self.textsize/2
        pygame.draw.rect(screen, self.backcolor, self.rect)# Draw the text box
        pygame.draw.rect(screen, self.wordcolor, self.rect, 1)# Draw the text box outline
        
        # Update rects and surfaces
        for surf in self.textsurfs:
            if not self.textsurfs.index(surf) == self.cursorpos:
                screen.blit(surf, curpos)
                self.textrects[self.textsurfs.index(surf)].topleft = curpos
            else:
                rect = self.textrects[self.textsurfs.index(surf)]
                rect.topleft = curpos
                surf = self.font.render(str(self.data[self.textsurfs.index(surf)]), True, self.selectedcolor)
                screen.blit(surf, curpos)
            curpos[1] += self.textsize
        e = event
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                if self.cursorpos > 0:
                    self.cursorpos -= 1
            elif e.key == pygame.K_DOWN:
                if self.cursorpos < len(self.data)-1:
                    self.cursorpos += 1
            elif e.key == pygame.K_SPACE:
                self.selected = self.data[self.cursorpos]
        elif e.type == pygame.MOUSEMOTION:
            mousepos = pygame.mouse.get_pos()
            for rect in self.textrects:
                if rect.collidepoint(mousepos):
                    self.cursorpos = self.textrects.index(rect)
        elif e.type == pygame.MOUSEBUTTONDOWN:
            self.selected = self.data[self.cursorpos]
        elif e.type == pygame.QUIT:
            self.selected = pygame.QUIT
        return
################################################################################################################################################################
class dummysound():
    def play(self):
        pass

try:
    phase = pygame.mixer.Sound('cool_phase.ogg')
except pygame.error:
    phase = dummysound()
    print 'Error: can\'t load phase.ogg'
try:
    spap = pygame.mixer.Sound('spap.ogg')
except pygame.error:
    spap = dummysound()
    print 'Error: can\'t load spap.ogg'
try:
    die = pygame.mixer.Sound('die.ogg')
except:
    die = dummysound()
    print 'Error: can\'t load die.ogg'

def menu():
    global screen, black, white, clock, Menu
    titlemenu = Menu([20, 65], wordcolor=[255, 0, 0], selectedcolor=[255, 255, 0], data=['1-Player game', '2-Player game', 'Quit'])
    screen.fill(black)
    font = pygame.font.Font(None, 32)
    screen.blit(font.render('The controls are: W-S for Player 1', True, white, black), [0, 0])
    screen.blit(font.render('Up-Down for Player 2. Solo: W-S', True, white, black), [0, 32])
    pygame.display.flip()
    while not titlemenu.selected:
        titlemenu.update(screen, pygame.event.poll())
        clock.tick(30)
        pygame.display.flip()
    if titlemenu.selected == '1-Player game':
        newGame()
    elif titlemenu.selected == '2-Player game':
        newGame(True)
    else:
        pygame.quit()
        sys.exit()
def newGame(twoplayer=False):
    global white, black
    class Paddle():
        def __init__(self, upkey, downkey):
            global screen
            self.area = [screen.get_width(), screen.get_height()]
            self.pos = [0, self.area[1]/2]
            self.rect = Rect((self.pos), (10, 40))
            self.speed = 5
            self.score = 0
            self.upkey, self.downkey = upkey, downkey
        def update(self):
            global screen, white
            keys = pygame.key.get_pressed()
            if keys[self.upkey]:
                if self.rect.top > 20:
                    self.rect.top -= self.speed
            elif keys[self.downkey]:
                if self.rect.bottom < self.area[1]-20:
                    self.rect.bottom += self.speed
            pygame.draw.rect(screen, blue, self.rect)
            return
    
    class Enemy():
        def __init__(self):
            global screen
            self.area = [screen.get_width(), screen.get_height()]
            self.pos = [self.area[0]-10, self.area[1]/2]
            self.rect = Rect((self.pos), (10, 40))
            self.speed = 5
            self.score = 0
        def update(self, ball):
            global screen, white

            # Enemy will use the closest ball
            balls = copy.copy(ball.container)
            best_so_far = self.area[0]
            closest_ball = None
            for each in balls:
                distance = self.area[0] - math.sqrt((self.rect.centerx - each.rect.centerx)**2 +
                                                    (self.rect.centery - each.rect.centery)**2)
                if distance < best_so_far:
                    closest_ball = each

            if closest_ball.rect.centery > self.rect.centery:
                if self.rect.top > 20:
                    self.rect.centery -= self.speed
            if closest_ball.rect.centery < self.rect.centery:
                if self.rect.bottom < self.area[1]-20:
                    self.rect.centery += self.speed
            pygame.draw.rect(screen, red, self.rect)
            return

    class Ball():
        def __init__(self, multiball=None):
            global screen
            self.pos = [screen.get_width()/2, screen.get_height()/2]
            self.center = self.pos
            self.rect = Rect((self.pos), (15, 15))
            self.speed = [random.randint(-6, 6), random.randint(-6, 6)]
            while self.speed[0] == 0:
                self.speed[0] = random.randint(-6, 6)
            while self.speed[1] == 0:
                self.speed[1] = random.randint(-6, 6)
            self.area = [screen.get_width(), screen.get_height()]
            # self.paddlecols = 0
            self.wallcols = 0  # The number of collisions with walls
            self.multiball = multiball
            self.color = random_color()

        def update(self, paddle, enemy):
            global screen, white, phase, spap, die
            if self.rect.top <= 0 or self.rect.bottom >= self.area[1]:
                # Collision with top or bottom
                self.speed[1] = -self.speed[1]
                if self.speed[1] < 0:
                    self.speed[1] -= 1
                elif self.speed[1] > 0:
                    self.speed[1] += 1
            if self.rect.right >= self.area[0]:
                # Collision with the right wall
                phase.play()
                self.wallcols += 1
                self.rect.right = self.area[0] - 1
                self.speed[0] = -self.speed[0]
                self.multiball.add_ball(self)
            elif self.rect.left <= 0:  
                # Collision with the left wall
                phase.play()
                self.wallcols += 1
                self.rect.left = 1
                self.speed[0] = -self.speed[0]
                self.multiball.add_ball(self)
            if self.rect.colliderect(paddle.rect) or self.rect.colliderect(enemy.rect):
                # Collision with paddle or enemy
                if self.rect.colliderect(paddle.rect):
                    die.play()
                    enemy.score += 1
                    self.multiball.reset = True
                elif self.rect.colliderect(enemy.rect):
                    die.play()
                    paddle.score += 1
                    self.multiball.reset = True
            if self.speed[0] > 6:
                self.speed[0] = 6
            elif self.speed[0] < -6:
                self.speed[0] = -6
            elif self.speed[1] > 6:
                self.speed[1] = 6
            elif self.speed[1] < -6:
                self.speed[1] = -6

            self.rect = self.rect.move(self.speed)
            pygame.draw.rect(screen, self.color, self.rect)
            return

    class MultiBall(object):
        def __init__(self, number_of_balls=1, maxbolls=100):
            self.number_of_balls, self.maxbolls = number_of_balls, maxbolls
            self.container = []
            for _ in range(self.number_of_balls):
                self.container.append(Ball(self))
            self.rect, self.center = self.container[0].rect, self.container[0].center
            self.reset = False

        def update(self, paddle, enemy):
            if self.reset:
                self.container = []
                for _ in range(self.number_of_balls):
                    self.container.append(Ball(self))
                self.reset = False
            [ball.update(paddle, enemy) for ball in self.container]

        def add_ball(self, parent):
            if len(self.container) < self.maxbolls:
                if (parent.wallcols < 3):
                    return
                new_ball = Ball(self)
                new_ball.rect =  parent.rect.copy()
                if (new_ball.rect.x > screen.get_width() / 2):
                    while new_ball.speed == parent.speed:
                        new_ball.speed[0] = random.randint(-6, -1)
                elif (new_ball.rect.x < screen.get_width() / 2):
                    while new_ball.speed == parent.speed:
                        new_ball.speed[0] = random.randint(1, 6)
                parent.wallcols = 0
                self.container.append(new_ball)

    ball = MultiBall()
    paddle = Paddle(pygame.K_w, pygame.K_s)
    paddle_two = Paddle(pygame.K_UP, pygame.K_DOWN)
    paddle_two.pos = [screen.get_width()-30, screen.get_height()/2]
    paddle_two.rect.center = paddle_two.pos
    enemy = Enemy()
    gameLoop(paddle, enemy, ball, twoplayer, paddle_two)
    startOver()
def gameLoop(paddle, enemy, ball, twoplayer, paddle_two):
    global screen, white, black, clock
    paddlescore = pygame.font.Font(None, 32)
    enemyscore = pygame.font.Font(None, 32)
    topscore = 0
    screen.fill(black)
    screen.blit(paddlescore.render('3', True, random_color()), ball.center)
    pygame.display.flip()
    time.sleep(1)
    screen.fill(black)
    screen.blit(paddlescore.render('2', True, random_color()), ball.center)
    pygame.display.flip()
    time.sleep(1)
    screen.fill(black)
    screen.blit(paddlescore.render('1', True, random_color()), ball.center)
    pygame.display.flip()
    time.sleep(1)
    screen.fill(black)
    screen.blit(paddlescore.render('GO!', True, random_color()), ball.center)
    pygame.display.flip()
    time.sleep(0.5)
    while not topscore > 9:
        screen.fill(black)
        paddle.update()
        if twoplayer:
            paddle_two.update()
            ball.update(paddle, paddle_two)
        else:
            enemy.update(ball)
            ball.update(paddle, enemy)
        pygame.draw.line(screen, white, [screen.get_width()/2, 0], [screen.get_width()/2, screen.get_height()])
        if twoplayer:
            scores = [paddle.score, paddle_two.score]
        else:
            scores = [paddle.score, enemy.score]
        topscore = sorted(scores, reverse=True)
        topscore = topscore[0]
        screen.blit(paddlescore.render(str(paddle.score), True, white), [270, 0])
        if twoplayer:
            screen.blit(enemyscore.render(str(paddle_two.score), True, white), [360, 0])
        else:
            screen.blit(enemyscore.render(str(enemy.score), True, white), [360, 0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(40)
        pygame.display.flip()
    screen.fill(black)
    if not twoplayer:
        if paddle.score == topscore:
            screen.blit(paddlescore.render('You Won! You beat the machine, proving that YOU', True, white, black), [0, 0])
            screen.blit(paddlescore.render('are the Master Pong Player! Well, not really.', True, white, black), [0, 32])
            screen.blit(paddlescore.render('But it was a nice thought. (Press any key to', True, white, black), [0, 64])
            screen.blit(paddlescore.render('return to the menu).', True, white, black), [0, 98])
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        menu()
        else:
            screen.blit(paddlescore.render('You Lost! This bucket of bolts beat a smart human like', True, white, black), [0, 0])
            screen.blit(paddlescore.render('yourself! Too bad! Press any key to return to menu.', True, white, black), [0, 32])
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        menu()
    else:
        if paddle.score == topscore:
            screen.blit(paddlescore.render('Player 1 won! (left side). Press any key to', True, white, black), [0, 0])
            screen.blit(paddlescore.render('to menu.', True, white, black), [0, 32])
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        menu()
        else:
            screen.blit(paddlescore.render('Player 2 won! (right side). Press any key to', True, white, black), [0, 0])
            screen.blit(paddlescore.render('to menu.', True, white, black), [0, 32])
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        menu()

if __name__ == '__main__':
    menu()

import collections
import math
import random
import pygame


# initialise pygame
pygame.init()

# set screen
width = 500
height = 500
rows = 20
columns = 20
screen = pygame.display.set_mode((width, height))

class position:
    x = 0
    y = 0 
        
    def __init__(self, X, Y):
        self.x = X
        self.y = Y

    def draw(self, surface, colour=(255,0,255)):
        scale = width//rows
        i = self.x
        j = self.y
        pygame.draw.rect(surface, colour, (scale*(i+1), scale*(j+1), scale-2, scale-2))

    def move(self, dX, dY):
        self.x += dX
        self.y += dY
        
class snake():
    body = collections.deque()
    dx = 0
    dy = 0
    food = position(10,15)
    score = 0
    highScore = 0

    def __init__(self):
        self.body.append(position(9,9))
        self.dx = 1
        self.dy = 0
        self.randomiseFood()
        self.score = 0
        self.highScore = 0

    # Reset Snake
    def reset(self):
        print("Score:",self.score, "\tHighScore: ",self.highScore)
        self.body = collections.deque()
        self.body.append(position(9,9))
        self.dx = 1
        self.dy = 0
        self.randomiseFood()
        self.score = 0

    # Print snake and food
    def draw(self, surface):
        for pos in self.body:
            pos.draw(surface, (255,0,0))
        # Purple head
        self.body[0].draw(surface,(160,32,240))
        
        # Green food
        self.food.draw(surface, (0, 255, 0))

    # Randomise food position
    def randomiseFood(self):
        # Randomly choose positions until food is not on a square occupied by the snake
        while True:
            x = random.randrange(-1,rows-1)
            y = random.randrange(-1,rows-1)
            tempPos = position(x,y)
            unique = True
            for pos in self.body:
                if pos.x == x and pos.y == y:
                    unique = False
                    break
                
            if unique:
                self.food = tempPos
                break

    # Eat food
    def eat(self):
        if self.body[0].x == self.food.x and self.body[0].y == self.food.y:
            self.body.append(self.body[-1])
            self.randomiseFood()
            self.score +=1
            if self.score > self.highScore:
                self.highScore = self.score
         
    # Move snake
    def move(self):
        # Deal with key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT] and self.dx!=1:
                    self.dx = -1
                    self.dy = 0
                elif keys[pygame.K_RIGHT] and self.dx!=-1:
                    self.dx = 1
                    self.dy = 0
                elif keys[pygame.K_UP] and self.dy!=1:
                    self.dy = -1
                    self.dx = 0
                elif keys[pygame.K_DOWN] and self.dy!=-1:
                    self.dy = 1
                    self.dx = 0

        # insert newPos at front and delete back of body
        newPos = position(self.dx + self.body[0].x, self.dy + self.body[0].y) 
        self.body.appendleft(newPos)
        self.body.pop()

        # Handle eating the apple
        self.eat()

        # check if snake hits boundary and reset if it does
        head = self.body[0]
        if head.x<-1 or head.x>=19 or head.y<-1 or head.y>=19:
            self.reset()

        # Check if snake head hits body at a point and cut this part off
        length = len(self.body)
        num = 0
        if length>1:
            for i,pos in enumerate(self.body):
                if i!=0 and pos.x == head.x and pos.y == head.y:                       
                    num = length - i - 1
                    self.score -=num
            while num>0:                                                 
                self.body.pop()    
                num-=1
                  
# Print score
font = pygame.font.Font('freesansbold.ttf', 22)
def showScore(x, y, score):
    text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, (x, y))

def showHighScore(x, y, score):
    text = font.render("High Score: " + str(score), True, (255, 255, 255))
    screen.blit(text, (x, y))

# Print screen
def drawWindow():
    global screen
    screen.fill((0,0,0))
    showScore(40,10,s.score)
    showHighScore(300,10,s.highScore)
    s.move()
    s.draw(screen)
    pygame.display.update()

     
def main():
    global s
    s = snake()
    while(True):
        pygame.time.delay(100)
        drawWindow()
        

main()
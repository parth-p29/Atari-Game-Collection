import pygame

import random
import pygame, sys, os


pygame.init()
window = pygame.display.set_mode((800,600))
pygame.display.set_caption("Color Pong!")
font = pygame.font.Font(None, 60)

colors = {

    1: (128, 168, 255),

    2: (255, 255, 102),        #dictionary which will stores all the 3 possible colors

    3: (128, 255, 170)

    }

##border_sound = pygame.mixer.Sound('263133__pan14__tone-beep.wav')

##game_music = pygame.mixer.music.load('music.mp3')
##pygame.mixer.music.play(-1)

class Paddle:

    def __init__(self, surface, color, x_pos, y_pos, length, width):

        self.surface = surface
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.length = length
        self.width = width
        self.color = color

    def drawRect(self):

        pygame.draw.rect(self.surface, self.color, (self.x_pos, self.y_pos, self.length, self.width))
    
    def changeColor(self, new_color):

        self.color = new_color

    def movePaddle(self, new_y):

        self.y_pos = new_y                   
        if self.y_pos <= 0:                  #allows the users paddle to move corresponding to the y-position of the mouse
            self.y_pos = 2

        elif user_paddle.y_pos +60 >= 555:
                self.y_pos = 508   #the self.y_pos refers is the top left location of the paddle so you need to make boundaries according to that
   
class Ball:

    def __init__(self, surface, color, x_pos, y_pos, radius):

        self.surface = surface
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius

    def drawBall(self):

        pygame.draw.circle(self.surface, self.color, (self.x_pos, self.y_pos), self.radius)

    def paddle_collision(self, userPaddle, computerPaddle):

        if self.x_pos < 22 and ((self.y_pos < userPaddle.y_pos +90) and (self.y_pos > userPaddle.y_pos)): #if the ball is within the paddles boundaries it will return True (for collision detected)           
            return 'u'

        if self.x_pos > 778 and ((self.y_pos < computerPaddle.y_pos +90) and (self.y_pos > computerPaddle.y_pos)):
            return "c"

    def changeColor(self, random_color):

        self.color = colors[random_color]
        
class Score:

    def __init__(self, points):
        self.point = points
        
    def addPoint(self):
        self.point += 1
        
    def displayText(self):
        text = font.render(str(self.point), False, [255, 255, 255])
        return text
        

user_paddle = Paddle(window, (255,255,255), 10, 250, 12, 90)
computer_paddle = Paddle(window, (255,255,255), 780,250,12,90)                              #initllizes the physical objects in the game
game_ball = Ball(window, (255,255,255), random.randint(200,300),random.randint(100,400), 8)

cpaddle_speed = 5

ball_x = 5  #the ball's x and y velocties
ball_y = 5

user_score = Score(0)     #intilizes the score
computer_score = Score(0)

times_clicked = 1
#####################################################################################################################################################################

while True: #main loop

    pygame.time.wait(8) #sets a delay before next iteration

    
    for event in pygame.event.get(): #My event listener list

        
            #each event has a number (the type) if the type matches the correspnding event it will execute the following code 

        if event.type == pygame.QUIT: #if u want to quit out the display and you click the 'x' on the top right, the event number for that is '12'
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:       
            user_paddle.movePaddle(event.pos[1]-45)  #moves the user's paddle


        if event.type == 2:      
            user_paddle.changeColor(colors[times_clicked])
            times_clicked += 1
            if times_clicked == 4:
                times_clicked = 1
        
#####################################################################################################################################################################

    if game_ball.y_pos < computer_paddle.y_pos:
        computer_paddle.y_pos -= 7.2
        
        if computer_paddle.y_pos <= 0:
            computer_paddle.y_pos = 2

    elif game_ball.y_pos > computer_paddle.y_pos:     #Moves the computer Paddle

        computer_paddle.y_pos += 7.2
        
        if computer_paddle.y_pos + 90 >= 600:
            computer_paddle.y_pos = 508
        


#####################################################################################################################################################################                


    if game_ball.paddle_collision(user_paddle, computer_paddle) == 'u':      

            if game_ball.color == user_paddle.color:
                
                ball_y = random.randint(3,6)
                game_ball.y_pos += ball_y                             #Paddle Collison
                ball_x = random.randint(3,6)
                game_ball.x_pos += ball_x
                game_ball.changeColor(random.randint(1,3))
                computer_paddle.changeColor(game_ball.color)

            else:
                game_ball.x_pos = 400
                game_ball.y_pos = 300
                computer_score.addPoint()

                
    if game_ball.paddle_collision(user_paddle, computer_paddle) == 'c':
        
            ball_y = random.randint(3,6) *-1
            
            
            game_ball.y_pos += ball_y                             #Paddle Collison

            ball_x = random.randint(3,6) *-1
            game_ball.x_pos += ball_x
            game_ball.changeColor(random.randint(1,3))
            computer_paddle.changeColor(game_ball.color)

#####################################################################################################################################################################

    else:
        
        if game_ball.x_pos >= 800:
            
            user_score.addPoint()
            ball_x = random.randint(3,6) * -1
            game_ball.x_pos = 400
            game_ball.y_pos = 300
            
        elif game_ball.y_pos >= 600:

##            border_sound.play()
            ball_y = random.randint(3,6) * -1
            game_ball.y_pos += ball_y

        elif game_ball.x_pos <= 0:
            
            computer_score.addPoint()                             #border Collision and gives the correspnding person the point
            ball_x = random.randint(3,6) 
            game_ball.x_pos = 400
            game_ball.y_pos = 300
            
        elif game_ball.y_pos <= 0:

##            border_sound.play()
            ball_y = random.randint(3,6) 
            game_ball.y_pos += ball_y

        else:
            game_ball.x_pos += ball_x
            game_ball.y_pos += ball_y
                                 

#####################################################################################################################################################################

    window.blit(user_score.displayText(), (200,50))
    window.blit(computer_score.displayText(), (600, 50))

    pygame.draw.line(window, [255,255,255], (400,0), (400,600), 1)
    game_ball.drawBall()           
    user_paddle.drawRect()
    computer_paddle.drawRect()

    
    pygame.display.update()    
    window.fill([0,0,0])
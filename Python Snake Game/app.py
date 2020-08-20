import pygame
import random

pygame.init()
pygame.display.set_caption("Parth Patel - Snake Game!")

win_height = 500
win_width = 500
window = pygame.display.set_mode((win_height,win_width))
snakehead = pygame.transform.scale(pygame.image.load("snakehead.ico"), (25,25))
snakefood = pygame.transform.scale(pygame.image.load("snakefood.ico"), (25,25))
snakebody = pygame.transform.scale(pygame.image.load("snakebody.png"), (25,25))
bg = pygame.transform.scale(pygame.image.load("snakeBg.png"), (500,500))

class Block:    #Block class will provide instances of the snake body in the game

    def __init__(self, x_pos, y_pos, image):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = image  #takes 3 attributes of x/y pos and the image 

    def place_block(self):
       window.blit(self.image, (self.x_pos, self.y_pos)) #places the block on the window

    def didCollide(self, obj):
        if self.x_pos == obj.x_pos and self.y_pos == obj.y_pos: #checks for collision between the snakes body and the food
            return True

    def moveSnake(self, vel, dirX, dirY, current_dir):

        if current_dir =='HORIZONTAL':
            self.x_pos += vel * dirX    #moves the snake depending on the horizontal/vertical direction
        else:
            self.y_pos += vel * dirY

    def boundaries(self):
        if self.x_pos >= win_width:
            self.x_pos = 0

        elif self.x_pos <= 0:
            self.x_pos = 475

        elif self.y_pos >= win_height: 
            self.y_pos = 0

        elif self.y_pos <= 0:
            self.y_pos = 475

def grid():

    for i in range(1, 20):   
        pygame.draw.line(window, (255,255,255), (25 * i, 0), (25*i, win_height), 1)
        pygame.draw.line(window, (255,255,255), (0, 25 * i), (win_width, 25 * i), 1)    #draw grid on GUI

def restart(keys, text1, text2):

    window.blit(text1, ( (500 - text1.get_width()) // 2, ( (500 - text1.get_height()) // 2) - text2.get_height()))    #restart functions displays a game over screen upon the snakes death
    window.blit(text2, ( (500 - text2.get_width()) // 2, 150 ))

    if keys[pygame.K_SPACE]:
        main()

def main():

    def drawEverything():    #draws everthing for the player to see
        window.blit(bg, (0,0))  #sets the background of the game board

        gameover_label = font.render("GAME OVER. press space to restart", 1, (255, 255, 255))    
        score_label = font.render(f"Score: {score} ", 1, (255, 255, 255))   #sets up the text

        if lives <= 0:
            
            restart(key_press, gameover_label, score_label)   #if player dies it calls restart

        else:
            grid()
            for body in my_snake:      #otherwise it will draw the grid, snake head and body
                snake_head.place_block()
                body.place_block()

            snake_food.place_block()
        
        pygame.display.update()  #updates the display
        
    rand_pos = random.randint(0,19)*25
    my_snake = [ Block(rand_pos, rand_pos, snakehead), Block(rand_pos-25, rand_pos, snakebody), Block(rand_pos-50, rand_pos, snakebody) ]  #this list will hold the snakes body and head
    snake_food = Block( (random.randint(0,19)*25) , (random.randint(0,19)*25), snakefood)   #the foods random location on the screen
    snake_head = my_snake[0]
    snake_vel = 25
    dir_x = 1                                #veriables to hold the snakes speed, score, life, direction, and previous location to add a growing mech for the snake
    dir_y = 1
    prevX = my_snake[0].x_pos
    prevY = my_snake[0].y_pos
    score = 0 
    lives = 1
    current_dir = 'HORIZONTAL' #checks whether it is going vertical or horizontal
    run = True
    font = pygame.font.SysFont("comicsans", 40)

    while run:

        pygame.time.delay(90)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key_press = pygame.key.get_pressed()
        if key_press[pygame.K_RIGHT]:

            current_dir = 'HORIZONTAL'
            dir_x = 1

        elif key_press[pygame.K_LEFT] :

            current_dir = 'HORIZONTAL'                  #this is how the snake will move, based on the players key events
            dir_x = -1

        elif key_press[pygame.K_UP]:

            current_dir = 'VERTICAL'
            dir_y = -1

        elif key_press[pygame.K_DOWN]:

            current_dir = 'VERTICAL'
            dir_y = 1

        #insert function adds the new element in the list at that certain index which is indicated
        my_snake.insert(1, Block(prevX, prevY, snakebody))   #it attaches a new block to the snake list (as the body) at the previous position of the snakes head

        if snake_head.didCollide(snake_food):

            snake_food.x_pos = random.randint(0,19)*25 
            snake_food.y_pos = random.randint(0,19)*25     #if the head collides with the food, the new body block will stay, or else it will be popped off the snake list
            score += 1
        else:
            my_snake.pop()

        snake_head.moveSnake(snake_vel, dir_x, dir_y, current_dir)  #moves the snakes head, the body will follow
        prevX = snake_head.x_pos
        prevY = snake_head.y_pos #sets the prev position of the head again, so that the body can follow

        for body in my_snake[1:]:
            if snake_head.didCollide(body):  #if the snakes head touches the body, it will end the game
                lives -= 1

        drawEverything()

main()
pygame.quit()
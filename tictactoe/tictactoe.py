import pygame
pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Tic Tac Toe")
class Player:

    def __init__(self, placement):

        self.score = 0
        self.placement = placement

    def scoreIncrease(self):
        self.score += 1

def drawGame():

    pygame.draw.line(window, (255, 255, 255), (165, 10), (165, 490), 2)
    pygame.draw.line(window, (255, 255, 255), (330, 10), (330, 490), 2)
    pygame.draw.line(window, (255, 255, 255), (10, 165), (490, 165), 2)
    pygame.draw.line(window, (255, 255, 255), (10, 330), (490, 330), 2)
    pygame.display.update()

def placeMove(x, y, color, state):

    if x > 330:

        if y > 330:
            pygame.draw.rect(window, color, (367.5, 367.5, 100, 100))
            gameboard[2][2] = state

        elif y > 165 and y < 330:

            pygame.draw.rect(window, color, (367.5, 202.5, 100, 100))
            gameboard[1][2] = state

        else:
            pygame.draw.rect(window, color, (367.5, 37.5, 100, 100))
            gameboard[0][2] = state

    elif x > 165 and x < 330:

        if y > 330:
            pygame.draw.rect(window, color, (202.5, 367.5, 100, 100))
            gameboard[2][1] = state

        elif y > 165 and y < 330:

            pygame.draw.rect(window, color, (202.5, 202.5, 100, 100))
            gameboard[1][1] = state

        else:
            pygame.draw.rect(window, color, (202.5, 37.5, 100, 100))
            gameboard[0][1] = state

    else:

        if y > 330:
            pygame.draw.rect(window, color, (37.5, 367.5, 100, 100))
            gameboard[2][0] = state

        elif y > 165 and y < 330:

            pygame.draw.rect(window, color, (37.5, 202.5, 100, 100))
            gameboard[1][0] = state

        else:
            pygame.draw.rect(window, color, (37.5, 37.5, 100, 100))
            gameboard[0][0] = state

def winCheck(state):

    rcount = 0
    gcount = 0
    ri = 0
    gi = 0
   
    # horizontal check
    for row in gameboard:

        for tile in row:

            if state == 1:

                if tile == 1:
                    gcount += 1

            elif state == 0:

                if tile == 0:
                    rcount += 1
        if rcount == 3 or gcount == 3:
            return True

        else:
            rcount = 0
            gcount = 0


    # vertical check
    for x in range(3):

        for y in range(3):

            if state == 1:

                if gameboard[y][x] == 1:
                    gcount += 1

            elif state == 0:

                if gameboard[y][x] == 0:
                    rcount += 1

        if rcount == 3 or gcount == 3:
            return True
        else:
            rcount = 0
            gcount = 0

    
    #diagonal check
    for tile in range (3):

        if state == 1:
            
            if gameboard[tile][tile] == 1:
                gcount += 1

        else:
            if gameboard[tile][tile] == 0:
                rcount +=1
        

    if rcount == 3 or gcount == 3:
        return True
        
    else:
        rcount = 0
        gcount = 0

    
    for tile in range(2,-1,-1):
        

        if state == 1:
            if gameboard[gi][tile]==1:
                gcount += 1
                
                gi += 1
            else:
                gi+=1
        
        else:
            if gameboard[ri][tile]==0:
                rcount +=1
                
                ri += 1
            else:
                ri+=1

    if rcount == 3 or gcount == 3:
        return True
    else:
        rcount = 0
        gcount = 0
        gi = 0
        ri = 0

green = (88, 235, 52)
red = (222, 67, 67)

gameboard = [[[], [], []],
             [[], [], []],
             [[], [], []]]

run = True
player1 = Player('green')
player2 = Player('red')
turn = True

# main loop
while run:

    pygame.time.delay(50)

    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]

    if winCheck(1):
        print('Green Won!')
        break

    elif winCheck(0):
        print('Red Won!')
        break

    else:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            else:
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if turn:

                        placeMove(mouseX, mouseY, green, 1)
                        turn = False

                    else:

                        placeMove(mouseX, mouseY, red, 0)
                        turn = True

    drawGame()
pygame.quit()

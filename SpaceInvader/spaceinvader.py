import pygame
import time
import random
pygame.font.init()

pygame.init()
window = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Space Invaders!")

bg = pygame.image.load('gamepics/spaceinvaderbg.png') #background


#player
rocket = pygame.transform.scale(pygame.image.load("gamepics/rocketship.ico"), (85, 85))
laser = pygame.transform.scale(pygame.image.load("gamepics/pixel_laser_yellow.png"), (49, 80))

#enemy
enemy = pygame.transform.scale(pygame.image.load("gamepics/enemy.png"), (75,75)) 
enemy_laser = pygame.image.load("gamepics/pixel_laser_red.png")



class Character:

    def __init__(self, x_pos, y_pos, vel):

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.vel = vel
        self.character_img = None
        self.lasers = []
        self.cool_down = 0
        

    def draw(self):
        window.blit(self.character_img, (self.x_pos, self.y_pos))
        for index in self.lasers:
            index.drawLaser()


    def prepareLasers(self):

        ship_gun = Laser(self.x_pos, self.y_pos, laser, 2)
        self.lasers.append(ship_gun)

    def shoot(self, target):

        for index in self.lasers:
            index.moveLaser()

            if index.y_pos <= 0:
                self.lasers.remove(index)

            if index.collide(target):
                self.lasers.remove(index)

                return True


class Laser:

    def __init__(self, lx, ly, laser_img, vel):
        self.x_pos = lx
        self.y_pos = ly
        self.vel = vel
        self.laser_img = laser_img
        self.mask = pygame.mask.from_surface(self.laser_img)

    def drawLaser(self):
        window.blit(self.laser_img, (self.x_pos + 21, self.y_pos - 45))
    
    def moveLaser(self):
        self.y_pos-=self.vel

    def collide(self, obj):

        return didCollide(self, obj)


class Rocket(Character):

    def __init__(self, x_pos, y_pos, vel):

        super().__init__(x_pos, y_pos, vel)
        self.character_img = rocket
        self.mask = pygame.mask.from_surface(self.character_img)
        self.health = 100


    def moveLeftX(self, keys):

        if keys[pygame.K_LEFT] and self.x_pos > 0:
            self.x_pos -= self.vel

    def moveRightX(self, keys):

        if keys[pygame.K_RIGHT] and self.x_pos < 1280-85:
            self.x_pos += self.vel

    def moveUpY(self, keys):

        if keys[pygame.K_UP] and self.y_pos > 350:
            self.y_pos -= self.vel

    def moveDownY(self, keys):

        if keys[pygame.K_DOWN] and self.y_pos < 720-85:
            self.y_pos += self.vel



class EnemyShip(Character):

    def __init__(self, x_pos, y_pos, vel):
        super().__init__(x_pos, y_pos, vel)
        self.character_img = enemy
        self.mask = pygame.mask.from_surface(self.character_img)

    def enemyMove(self):
        self.y_pos += self.vel


def gameRestart(keys, text):

    window.blit(text, ( (1280//2)- (text.get_width()) + 270, 720//2))

    if keys[pygame.K_SPACE]:
        main()


def didCollide(ob1, ob2):

    offset_x = ob2.x_pos - ob1.x_pos
    offset_y = ob2.y_pos - ob1.y_pos

    return ob1.mask.overlap(ob2.mask, (offset_x, offset_y)) 
    


def main():

    run_game = True

    enemy_vel = 3  #enemy velocity
    enemies = []  #array that holds all the enemy ships
    wave_length = 1 #num of enemies in each wave

    FPS = 60
    lives = 3
    wave = 0
    vel = 10
    font = pygame.font.SysFont("comicsans", 40)
    clock = pygame.time.Clock()

    user_rocket = Rocket(600, 500, vel)


    def drawWindow():

        window.blit(bg, (0,0))

        #draw text
        lives_label = font.render(f"lives: {lives}", 1, (255, 255, 255))
        wave_label = font.render(f"Wave: {wave}", 1, (255, 255, 255))
        health_label = font.render(f"Health: {user_rocket.health}%", 1, (255, 255, 255))
        gameover_label = font.render("GAME OVER. press space to restart", 1, (255, 255, 255))

        if lives == 0:
            gameRestart(keys, gameover_label)
            
        else:
            window.blit(lives_label, (20,20))
            window.blit(wave_label, (20,60))
            window.blit(health_label, (20,100))

            for enemy_ship in enemies:   #for each enemy in the enemies array, it will draw all of them
                enemy_ship.draw() 


            #user ship 
            user_rocket.draw()
            
            
        pygame.display.update()


    while run_game:

        clock.tick(FPS)
    
        if user_rocket.health <= 0:
            lives -= 1
            user_rocket.health = 100


        if len(enemies) == 0:  #if all enemies die it will increase wave by 1
            wave += 1
            wave_length += 3 #increases the num of enemies in each wave by 5

            for index in range(wave_length):
                enemy_ship = EnemyShip(random.randrange(50, 1160), random.randrange(-1000, -200), enemy_vel)
                enemies.append(enemy_ship)


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run_game = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    user_rocket.prepareLasers()
                    
            
        keys = pygame.key.get_pressed()


        for enemy_ship in enemies:
            enemy_ship.enemyMove()
            if user_rocket.shoot(enemy_ship):
                enemies.remove(enemy_ship)
            
            if enemy_ship.y_pos > 780:
                enemies.remove(enemy_ship) #removes the current enemy ship in the enemies list
                user_rocket.health -= 5

            
        user_rocket.moveDownY(keys)
        user_rocket.moveUpY(keys)
        user_rocket.moveLeftX(keys)
        user_rocket.moveRightX(keys)
      
        drawWindow()
        

main()

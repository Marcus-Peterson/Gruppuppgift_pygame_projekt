from re import L
import pygame
import time
import os
from random import randint as RI

pygame.init()
collision_threshhold = 25
max_ball_speed = 5 
WHITE = (255,255,255)
FPS = 60
WIDTH, HEIGHT = 1280 , 720
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()#a group that holds all sprites,
#img_folder = os.path.join('assets\images')#path to image folder, saved as a variabel


#---------
brick_cols = 12
brick_rows = 6
brick_start = 16

bricks = [
    'assets/images/element_blue_rectangle_glossy.png',
    'assets/images/element_green_rectangle_glossy.png',
    'assets/images/element_red_rectangle_glossy.png',
    'assets/images/element_yellow_rectangle.png'
]

class Bricks:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.all_bricks = pygame.sprite.Group()

        for r in range(brick_rows):
            for c in range(brick_cols):
                brick = Brick(r, c)
                self.all_bricks.add(brick)
                self.all_sprites.add(brick)
    
    def check_collisions(self, ball):
        collision_list = pygame.sprite.spritecollide(ball, self.all_bricks, False)
        for brick in collision_list:
            ball.bounce()
            brick.kill()




class Brick:
    def __init__(self, row, col):
        super().__init__()
        self.x_pos = brick_start * (col * 64) * 32
        self.y_pos = brick_start * (row * 32) * 16
        self.image = pygame.image.load(bricks[row])
        self.rect = self.image.get_rect()
        self.rect.center = (self.x_pos, self.y_pos)

#---------

def draw_window():#fills the screen with color white and updates the screen 
    screen.fill((WHITE))

class board(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('assets','breakout_piece_blue.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (120,40))
        self.rect = self.image.get_rect()#creates a rect around image
        self.y_pos = HEIGHT -50
        self.x_pos = WIDTH /2
        self.rect.center = (self.x_pos, self.y_pos)
        self.direction = 0
        self.speed = 12 
    def update(self):
        if self.x_pos < 60:#60 is halv of board length in pixels
            self.x_pos = 60
        if self.x_pos > WIDTH -60:
            self.x_pos = WIDTH -60
        self.rect.center = (self.x_pos,self.y_pos)
    def move_left(self):
        self.x_pos -= self.speed
        self.direction = -1
    def move_right(self):
        self.x_pos += self.speed
        self.direction = 1
    
        
class ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x_pos = WIDTH / 2
        self.y_pos = HEIGHT / 2
        self.image = pygame.image.load(os.path.join('assets','ball_piece_blue.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (24,24))
        self.rect = self.image.get_rect()
        self.velocity = [RI(10,10), RI(10,10)]#self.velocity[0] is the first random for x pos and self.velocity[1] is the other random for y 
        self.rect.center = (self.x_pos, self.y_pos)
    def update(self):
        # 6 is halv of the ball's size in pixels 
        if self.x_pos < 6 or self.x_pos > WIDTH - 6: #if ball collide with left or rigth side it will reverse 
            self.velocity[0] = -self.velocity[0]
        if self.y_pos < 6: #if the ball collide with the top of the screen set the velocity to negative
            self.velocity[1] = -self.velocity[1]
        if self.velocity[0] == 0:#if the velociy reach 0 in either x or y direction, add velocity 
            self.velocity[0] += 1
        if self.velocity[1] == 0:
            self.velocity[1] += 1
        #sets the velocity to the current position so de ball will move acordingly 
        self.x_pos += self.velocity[0] 
        self.y_pos += self.velocity[1]
        self.rect.center = (self.x_pos, self.y_pos)
    def reset(self):# when the bal resets it will spawn in the center of the screen and have random direction(velocity)
        self.velocity = [RI(10,10), RI(10,10)]
        self.x_pos = WIDTH / 2
        self.y_pos = HEIGHT / 2
        self.rect.center = (self.x_pos, self.y_pos) 

    def check_board_collision(self,board):
         if self.rect.colliderect(board.rect):
            if abs(self.rect.bottom - board.rect.top) < collision_threshhold and self.velocity[1]>0:
                self.velocity[1] = -self.velocity[1]
                self.velocity[0] += board.direction
                if self.velocity[0] > max_ball_speed:
                    self.velocity[0] = max_ball_speed
                if self.velocity[0] < -max_ball_speed:
                    self.velocity[0] = -max_ball_speed
                else:   
                    self.velocity[0] *= -1

    #-------
    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = RI(-4, 4)
    #-------

    

    def is_out_bounds(self):
        return self.y_pos > HEIGHT


class player:
    pass

board = board()
ball = ball()
all_sprites.add(board,ball)
    
#create a wall




class Main:
    pass

    def main():
        running = True
        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                board.move_left()
            if key[pygame.K_RIGHT]:
                board.move_right()            
            
            
            
            

            ball.check_board_collision(board)
            if ball.is_out_bounds():
                ball.reset()
            all_sprites.update()#uppdates all sprites that is inside sprite.group()
            draw_window()#makes the bakground white
            #draw wall
            
            all_sprites.draw(screen)#prints/drwas out all sprites in sprite.group()
            pygame.display.update()       
          
    if __name__ == "__main__":
        main()
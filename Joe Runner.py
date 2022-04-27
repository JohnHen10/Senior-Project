import math
import pygame
import os
import random
import sys
import neat

pygame.init()

SCREEN_HEIGHT = 550
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
RUNNING = [pygame.transform.scale2x(pygame.image.load(os.path.join("Assets/Joe", "Joe Run 1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("Assets/Joe", "Joe Run 2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("Assets/Joe", "Joe Run 3.png")))]
JUMPING = [pygame.transform.scale2x(pygame.image.load(os.path.join("Assets/Joe", "Joe Jump 1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("Assets/Joe", "Joe Jump 2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("Assets/Joe", "Joe Jump 3.png")))]
SLIDING = pygame.transform.scale2x(pygame.image.load(os.path.join("Assets/Joe", "Joe Slide.png")))
BG = pygame.image.load(os.path.join("Assets/Other", "Ground.png"))
HILLSBG = pygame.image.load(os.path.join("Assets/Other", "BG.png"))
SMALL_BOX = pygame.image.load(os.path.join("Assets/Other", "Crate.png"))
BIG_BOX = [pygame.image.load(os.path.join("Assets/Other", "Big Crate 4.png")), pygame.image.load(os.path.join("Assets/Other", "Big Crate 3.png"))]
TOP_BOX = [pygame.image.load(os.path.join("Assets/Other", "Crate Top.png")), pygame.image.load(os.path.join("Assets/Other", "Crate Top 2.png"))]
FLYING = [pygame.image.load(os.path.join("Assets/Other", "Dragon Fly 1.png")), pygame.image.load(os.path.join("Assets/Other", "Dragon Fly 2.png")), pygame.image.load(os.path.join("Assets/Other", "Dragon Fly 3.png"))] 
OBJ = pygame.image.load(os.path.join("Assets/Gems", "Blue.png"))

FONT = pygame.font.Font('freesansbold.ttf', 20)

class Joe:
    X_POS = 550
    Y_POS = 410
    JUMP_VEL = 9

    def __init__(self, img=RUNNING[0]):
        self.image = img
        self.joe_run = True
        self.joe_jump = False
        self.joe_slide = False
        self.jump_vel = self.JUMP_VEL
        self.rect = pygame.Rect(self.X_POS-10, self.Y_POS-10, img.get_width()-20, img.get_height()-10)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.step_index = 0
        self.jump_index = 0
        self.slide_index = 0

    def update(self):
        if self.joe_run:
            self.run()
        if self.joe_jump:
            self.jump()
        if self.joe_slide:
            self.slide()
        if self.step_index >= 15:
            self.step_index = 0
        if self.jump_index >= 30:
            self.jump_index = 0
     
            
    def jump(self):
        self.image = JUMPING [self.jump_index // 10]
        self.jump_index += 1
        if self.joe_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel <= -self.JUMP_VEL:
            self.joe_slide = False
            self.joe_jump = False
            self.joe_run = True
            self.jump_vel = self.JUMP_VEL

    def run(self):
        self.image = RUNNING[self.step_index // 5]
        self.rect.x = self.X_POS 
        self.rect.y = self.Y_POS
        self.step_index += 1

    def slide(self):
        self.image = SLIDING
        self.rect.x = self.X_POS 
        self.rect.y = self.Y_POS + 5
        self.slide_index += 1
        
    def draw(self, SCREEN,):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(SCREEN, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
        for obstacle in obstacles:
            pygame.draw.line(SCREEN, self.color, (self.rect.x + 54, self.rect.y + 12), obstacle.rect.center, 2)
        for objective in objectives:
            pygame.draw.line(SCREEN, self.color, (self.rect.x + 54, self.rect.y + 12), objective.rect.center, 2)
             
class Dragon:
    X_POS = 22
    Y_POS = 275

    def __init__(self, img=FLYING[0]):
        self.img = img
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(), img.get_height())
        self.fly_index = 0
        self.dragon_fly = True

    def update(self):
        if self.dragon_fly:
            self.fly()
        #self.rect.x -= game_speed + 10
        if self.fly_index >= 18:
            self.fly_index = 0

    def fly(self):
        self.image = FLYING[self.fly_index // 6]
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.fly_index += 1
       

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))



class Objective:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(290, 450)
        self.color =(130,40,50)
        self.passed = False

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            objectives.pop()
    
    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)
        for obstacle in obstacles:
            pygame.draw.line(SCREEN, self.color, self.rect.center, obstacle.rect.center, 2)


class Obstacle:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.passed = False
    
    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):  
        SCREEN.blit(self.image, self.rect)


class SmallBox(Obstacle):
    def __init__(self, image):
        super().__init__(image)
        self.rect.y = 420

class TopBox(Obstacle):
    def __init__(self, image):
        super().__init__(image)
        self.rect.y = 100 



def remove(index):
    joes.pop(index)
    ge.pop(index)
    nets.pop(index)

   
def distance(pos_a, pos_b):
    dx = pos_a[0]-pos_b[0]
    dy = pos_a[1]-pos_b[1]
    return math.sqrt(dx**2+dy**2)
    

def main(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, joes, objectives, ge ,nets
    points = 0
    clock = pygame.time.Clock()

    dragons = [Dragon()]
    obstacles = []
    joes = []
    objectives =  []
    ge = []
    nets = []

    x_pos_bg = 0
    y_pos_bg = 480
    game_speed = 10

    for genome_id, genome in genomes:
        
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        joes.append(Joe())
        ge.append(genome)
        nets.append(net)
        genome.fitness = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 ==0 and game_speed < 35:
            game_speed += 1
        text = FONT.render(f'points: {str(points)}', True, (0, 0, 0))
        SCREEN.blit(text, (950, 50))

    def statistics():
        global joes, game_speed, ge
        text_1 = FONT.render(f'Joes Runnin:  {str(len(joes))}', True, (0, 0, 0))
        text_2 = FONT.render(f'Generation Number:  {pop.generation+1}', True, (0, 0, 0))
        text_3 = FONT.render(f'Game Speed:  {str(game_speed)}', True, (0, 0, 0))

        SCREEN.blit(text_1, (50, 100))
        SCREEN.blit(text_2, (50, 120))
        SCREEN.blit(text_3, (50, 140))

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if points == 10000:
            pygame.quit()
            sys.exit()

        SCREEN.fill(0)
        SCREEN.blit(HILLSBG, (0,0))

                
        for joe in joes:
            joe.update()
            joe.draw(SCREEN)

        for dragon in dragons:
            dragon.update()
            dragon.draw(SCREEN)

        if len(joes) == 0:
            break

        if len(obstacles) == 0:
            obstacles.append(TopBox(SMALL_BOX))
            obstacles.append(SmallBox(SMALL_BOX))

        if len(objectives) == 0:
            objectives.append(Objective(OBJ))

       

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            for i, joe in enumerate(joes): 
                if not obstacle.passed and obstacle.rect.x < joe.rect.x:
                    obstacle.passed = True
                    ge[i].fitness +=1
                if joe.rect.colliderect(obstacle.rect):
                    ge[i].fitness -= 10
                    remove(i)
                
                

        for objective in objectives:
            objective.draw(SCREEN)
            objective.update()
            for i, joe in enumerate(joes): 
                if joe.rect.colliderect(objective.rect):
                    points = points + 100
                    ge[i].fitness += 3
                    objectives.pop()
                    objectives.append(Objective(OBJ))
                    #if joe.rect.colliderect(objective.rect) == False and joe.rect.x > obstacle.rect.x:
                    #     ge[i].fitness -= 1
                if not objective.passed and objective.rect.x < joe.rect.x:
                    objective.passed = True
                    ge[i].fitness -= 3
                 

        user_input = pygame.key.get_pressed()

        for i, joe in enumerate(joes):
            ge[i].fitness += 0.01
            if not obstacle.passed or not objective.passed:
                output = nets[i].activate((joe.rect.y,
                                       distance((joe.rect.x, joe.rect.y),
                                        obstacle.rect.midtop),distance((joe.rect.x, joe.rect.y),
                                        objective.rect.center),distance(objective.rect.center,obstacle.rect.midtop)))
            if output[0] > 0.5 and joe.rect.y == joe.Y_POS:
                joe.joe_jump = True
                joe.joe_run = False
                #if objective.passed and obstacle.passed:
                  #  ge[i].fitness -= 5
               # if joe.rect.colliderect(objective.rect) == False and joe.rect.x > obstacle.rect.x:
               #     ge[i].fitness -= 1
        

        statistics()
        score()
        background()    
        clock.tick(30)
        pygame.display.update()
        
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(main, 50)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)

main()
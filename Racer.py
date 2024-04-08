#Импортируем нужные библиотеки
import pygame, sys
from pygame.locals import *
import random, time
 

#Инстализируем pygame
pygame.init()
 

#Устанавливаем кадры в секунду
FPS = 60
FramePerSec = pygame.time.Clock()
 
 
#Создаем и придаем значения для переменные
SCREEN_WIDTH = 570
SCREEN_HEIGHT = 650
SPEED = 5
SCORE = 0
 

#Текста которые мы используем в будущем
font = pygame.font.SysFont("Times New Roman", 60)
font_small = pygame.font.SysFont("Times New Roman", 20)
game_over = font.render("Game Over", True, 'Yellow')


#Задний фон в виде асфальта
background = pygame.image.load("asphalt.png")
 

#Разрешение экрана нашей игры
Screen = pygame.display.set_mode((570,650))


#Изменяем название нашей игры
pygame.display.set_caption("Racing Game")
 

#Создаем класс для встречного авто
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  
    
    #Функция для передвижений встречного авто
    def move(self):
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


#Создаем класс для монет
class Coins(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(('Yellow'))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
    
    #Функция для передвижений монет
    def move(self):
        global SCORE
        self.rect.move_ip(0, 20)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  


#Создаем класс для игрока 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    #Функция для передвижений нашего игрока    
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -3)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0,3)
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-6.5, 0)
        if self.rect.right < 570:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(6.5, 0)
                   
#Вызываем наши классы       
P1 = Player()
E1 = Enemy()
coin1 = Coins()

 
#Создаем группы
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(coin1)
coins_group = pygame.sprite.Group()
coins_group.add(coin1)  # Добавляем монету в группу спрайтов монет
 
#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 60)

#Game Loop
while True:
       
    #Cycles through all events occurring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5     
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
 
    Screen.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, 'Black')
    Screen.blit(scores, (10,10))
 
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        Screen.blit(entity.image, entity.rect)
        entity.move()
 
    # Обновление счета при столкновении игрока с монетой
    if pygame.sprite.spritecollide(P1, coins_group, False):
        SCORE += 1
    
    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.mp3').play()
        time.sleep(1)

        myscore = font.render(f"Your score: {SCORE}", True, 'Red')     

        Screen.fill('Black')
        Screen.blit(game_over, (138,250))
        Screen.blit(myscore, (138,300))
           
        pygame.display.update()
        for entity in all_sprites:
                entity.kill() 
        time.sleep(1.5)
        pygame.quit()
        sys.exit()  
          
                
         
    pygame.display.update()
    FramePerSec.tick(FPS)
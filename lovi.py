from pygame import *
from random import randint
from time import time as timer
from time import sleep
#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')

#шрифты и надписи
font.init()
font1 = font.SysFont("Arial", 80)
win = font1.render('YOU WIN!', 0, (255, 255, 255))
lose = font1.render('YOU LOSE!', 0, (180, 0, 0))
font2 = font.SysFont("Arial", 36)
text_ur1 = font2.render('Уровень 1', 0, (255, 255, 255))
text_ur2 = font2.render('Уровень 2', 0, (255, 255, 255))
text_ur3 = font2.render('Уровень 3', 0, (255, 255, 255))
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
    
        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
    
        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
#класс главного игрока
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
   
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    
#класс спрайта-добычи  
class Dobyacha(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        #исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

#класс спрайта-врага  
class Enemy1(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        #исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.kill()
              
clock = time.Clock()
FPS = 40
 
#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Лови мячи")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("fon2.jpg"), (win_width, win_height))
 
score = 0 #сбито кораблей
lost = 0 #пропущено кораблей
 
#создаем спрайты
korzina = Player("korz.png", 5, win_height - 150, 150, 150, 10)
 
dobychas1 = sprite.Group()
for i in range(1, 6):
    dobycha1 = Dobyacha("tenis_ball.png", randint(80, win_width - 80), 0, 30, 30, randint(3, 8))
    dobychas1.add(dobycha1)

dobychas2 = sprite.Group()
for i in range(1, 8):
    dobycha2 = Dobyacha("ufo.png", randint(80, win_width - 80), 0, 30, 30, randint(3, 8))
    dobychas2.add(dobycha2)

dobychas3 = sprite.Group()
for i in range(1, 5):
    dobycha3 = Dobyacha("asteroid.png", randint(80, win_width - 80), 0, 50, 50, randint(5, 9))
    dobychas3.add(dobycha3) 

vrags1 = sprite.Group()   
for i in range(3):
    vrag1 = Enemy1("bullet.png", randint(80, win_width - 80), randint(-100, 0), 100, 100, randint(5, 9))
    vrags1.add(vrag1) 
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
ur1 = True
ur2 = False
ur3 = False
rel_time = False
while run:
   #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
    if score < 10 and rel_time == False:
            pass
                     
    if  9 <= score <= 12 and rel_time == False : #если игрок сделал 5 выстрелов
        last_time = timer() #засекаем время, когда это произошло
        rel_time = True #ставим флаг перезарядки

    if not finish:
        window.blit(background,(0,0))
        korzina.update()
        korzina.reset()




        if ur1 == True:        
            dobychas1.update()
            dobychas1.draw(window)
            # window.blit(text_ur1, (300, 20))
            if sprite.spritecollide(korzina, dobychas1, True):
                score += 1
                dobycha1 = Dobyacha("tenis_ball.png", randint(80, win_width - 80), 0, 30, 30, randint(3, 8))
                dobychas1.add(dobycha1)
    
            #проверка уровня 2: сколько очков набрали?
            if score >= 10:
                if rel_time == True:
                    now_time = timer() #считываем время
    
                if now_time - last_time < 3: #пока не прошло 3 секунды выводим информацию о перезарядке
                    for mn in dobychas1:
                        mn.kill()
                    reload = font2.render('Уровень 2', 1, (150, 0, 0))
                    window.blit(reload, (260, 460))
                else:
                    rel_time = False #сбрасываем флаг перезарядки
                    ur1 = False

                    lost = 0
                    # time.delay(3000)
                    ur2 = True

        if ur2 == True:
            dobychas2.update()
            dobychas2.draw(window)
            # window.blit(text_ur2, (300, 20))
            if sprite.spritecollide(korzina, dobychas2, True):
                score += 1
                dobycha2 = Dobyacha("ufo.png", randint(80, win_width - 80), 0, 30, 30, randint(3, 8))
                dobychas2.add(dobycha2)
            #проверка уровня 3: сколько очков набрали?
            if score >= 30:
                ur2 = False
                ur3 = True
                lost = 0
                for mn in dobychas2:
                    mn.kill()


        if ur3 == True:
            dobychas3.update()
            dobychas3.draw(window)
            vrags1.update()
            vrags1.draw(window)
            window.blit(text_ur3, (300, 20))
            if sprite.spritecollide(korzina, dobychas3, True):
                score += 1
                dobycha3 = Dobyacha("asteroid.png", randint(80, win_width - 80), 0, 50, 50, randint(5, 9))
                dobychas3.add(dobycha3)
            if sprite.spritecollide(korzina, vrags1, True):
                finish = True
                window.blit(lose, (300, 200))
        if lost>= 7:
            finish = True
            window.blit(lose, (200, 200))


        #пишем текст на экране
        text = font2.render("Счет: " + str(score), 0, (255, 255, 255))
        window.blit(text, (10, 20))
    
        text_lose = font2.render("Пропущено: " + str(lost), 0, (255, 255, 255))
        window.blit(text_lose, (10, 50))    
           
        display.update()

    time.delay(50)
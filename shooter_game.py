
from pygame import *
from random import randint
from time import time as timer

window = display.set_mode((1000,700))
clock = time.Clock()
display.set_caption('Стрелялки')
background = transform.scale(image.load('galaxy.jpg'),(1000,700))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_music = mixer.Sound('fire.ogg')
font.init()
font = font.SysFont('Arial',35)
score = 0
miss = 0
class Gamer(sprite.Sprite):
    def __init__(self,gamer_image,gamer_x,gamer_y,size_x,size_y,gamer_step):
        super().__init__()
        self.image=transform.scale(image.load(gamer_image),(size_x,size_y))
        self.rect=self.image.get_rect()
        self.rect.x=gamer_x
        self.rect.y=gamer_y
        self.step=gamer_step
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(Gamer):
    def control(self):
        buttons = key.get_pressed()
        if buttons[K_a] and self.rect.x>0:
            self.rect.x -= self.step
        if buttons[K_d] and self.rect.x<920:
            self.rect.x += self.step
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.x+50,self.rect.y,15,20,15)
        bullets.add(bullet)
class Enemy(Gamer):
    def update(self):
        self.rect.y += self.step
        global miss
        if self.rect.y > 700:
            miss += 1
            self.rect.y = 0
            self.rect.x
class Enemy_1(Gamer):
    def update(self):
        self.rect.y += self.step
        if self.rect.y > 700:
            self.rect.y = 0
            self.rect.x
class Bullet(Gamer):
    def update(self):
        self.rect.y -= self.step
        if self.rect.y < 0:
            self.kill()


game = True 
finish = False
Tema = Player('rocket.png',460,600,100,100,10)
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy_1('asteroid.png',randint(80,920),0,80,80,randint(1,3))
    asteroids.add(asteroid)
monsters = sprite.Group()
for i in range(1,5):
    monster = Enemy('ufo.png',randint(0,920),0,80,80,randint(2,7))
    monsters.add(monster)
kol_billets = 0
r = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_l and kol_billets < 5 and r == False:
                kol_billets +=1
                fire_music.play()
                Tema.fire()
            if kol_billets >= 5 and r == False:
                start_t = timer()
                r = True 
    if finish != True:
        window.blit(background,(0,0))
        score_text = font.render('Счёт: '+str(score),True,(255,255,255))
        miss_text = font.render('Пропущено: '+str(miss),True,(255,255,255))
        window.blit(score_text,(10,10))
        window.blit(miss_text,(10,55))
        Tema.reset()
        Tema.control()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        if r == True:
            end_t = timer()
            if end_t-start_t <2:
                text_r = font.render('Пеееерезарядкаааааа',True,(255,255,255))
                window.blit(text_r,(500,350))
            else:
                r = False
                kol_billets = 0
        if sprite.spritecollide(Tema,monsters,False)or sprite.spritecollide(Tema,asteroids,False)or miss >= 10:
            finish = True
            text_lose = font.render('ВЫ ПРОДУЛИ!!!',True,(255,255,255))
            window.blit(text_lose,(500,350))
        babah = sprite.groupcollide(bullets,monsters,True,True)
        for i in babah:
            score += 1
            monster = Enemy('ufo.png',randint(80,920),0,80,80,randint(1,5))
            monsters.add(monster)
        if score >=50:
            finish = True
        display.update()
    clock.tick(60)
from pygame import *
from random import randint


window_width = 700
window_height = 500

window = display.set_mode((window_width,window_height))
display.set_caption("shooter")
background = transform.scale(image.load("back.jpg"), (window_width,window_height))

count = 0
missed = 0
mixer.init()
mixer.music.load("back_music.ogg")
mixer.music.play()
fire_sound = mixer.Sound("pew.ogg")
die_sound = mixer.Sound("killChicken.wav")

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width=65, height=65):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width,height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))


class Obstacle(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = -100
            self.rect.x = randint(30,645)
            self.speed = randint(1,3)

obstacles = sprite.Group()
for i in range(3):
    obstacles.add(Obstacle("egg.png", randint(10,625),10, randint(1,3),30,30))

class Player(GameSprite):
    rel_flag = False
    num_fire = 0
    def update(self):
        global recharge
        keys_pressed = key.get_pressed()

        if keys_pressed[K_a] and self.rect.x >= 10:
            self.rect.x -= self.speed

        if keys_pressed[K_d] and self.rect.x <= 625:
            self.rect.x += self.speed

        if keys_pressed[K_SPACE]:
            if self.rel_flag and recharge <= 120:
                self.num_fire = 0
                return 
            else:
                self.rel_flag = False      
            if recharge >= 10:
                self.fire()
                recharge = 0
                self.num_fire += 1
                if self.num_fire >= 10:
                    self.rel_flag = True
    
    def fire(self):
        fire_sound.play()
        bullets.add(Bullet("laser.png",self.rect.centerx - 10, self.rect.y -35, 15,25,25))

class Bullet(GameSprite):
    def update(self):    
        self.rect.y -= self.speed
        if self.rect.y < -self.rect.height:
            self.kill

bullets = sprite.Group()


class Enemy(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = -self.rect.width
            self.rect.x = randint(10,625)
            missed += 1
        self.speed = randint(1,3)

hero = Player("hero.png", window_width//2 , 400, 6)

enemies = sprite.Group()
for i in range(5):
    enemies.add(Enemy("enemy.png", randint(10,625),10, randint(0,3)))

clock = time.Clock()
game = True
finish = False
FPS = 60
recharge = 0

font.init()
loose_text = font.SysFont("Arial", 40).render("GAME OVER:(", True, (224,224,224))
win_text = font.SysFont("Arial", 40).render("WIN!!!", True, (224,224,224))
loose_rect = loose_text.get_rect()
win_rect = win_text.get_rect()

while game:
    if not finish:        
        window.blit(background, (0,0))

        hero.update()
        hero.reset()

        enemies.update()
        enemies.draw(window)
        
        bullets.update()
        bullets.draw(window)

        obstacles.update()
        obstacles.draw(window)

        count_text = font.SysFont("Arial", 40).render(f"count: {count}", True, (224,224,224))
        missed_text = font.SysFont("Arial", 40).render(f"missed: {missed}", True, (224,224,224))

        window.blit(count_text,(10,10))
        window.blit(missed_text,(10,35))

    for e in event.get():
        if e.type == QUIT:
            game = False

    if missed == 10:
        finish = True
        enemies.empty()
        display.update()
        window.blit(loose_text,(window_width//2 - loose_rect.width//2,window_height//2))
    if count == 20:
        finish = True
        enemies.empty()
        display.update()
        window.blit(win_text,(window_width//3 + 60,window_height//2))

    if len(sprite.groupcollide(enemies, bullets, True, True)) != 0:
        enemies.add(Enemy("enemy.png", randint(10,625),10, randint(0,3)))
        die_sound.play()
        count += 1

    if len(sprite.spritecollide(hero, enemies, False)):
        enemies.empty()
        window.blit(background, (0,0))
        hero.reset()
        display.update()
        finish = True
        window.blit(loose_text,(window_width//2 - loose_rect.width//2,window_height//2))

    if len(sprite.spritecollide(hero, obstacles, True)):
        obstacles.add(Obstacle("egg.png", randint(10,625),10, randint(1,3),30,30))
        
    keys_pressed = key.get_pressed()

    if keys_pressed[K_r]:
        enemies.empty()
        bullets.empty()
        obstacles.empty()
        finish = False
        for i in range(5):
            enemies.add(Enemy("enemy.png", randint(10,625),10, randint(0,3)))
        for i in range(3):
            obstacles.add(Obstacle("egg.png", randint(10,625),10, randint(1,3),30,30))
        missed = 0
        count = 0
        hero.rect.x = window_width//2

    recharge += 1  

    display.update()
    clock.tick(FPS)

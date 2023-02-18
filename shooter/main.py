from pygame import *
from random import randint



window_width = 700
window_height = 500

window = display.set_mode((window_width,window_height))
display.set_caption("shooter")
background = transform.scale(image.load("back.jpg"), (window_width,window_height))

count = 0
missed = 0
#mixer.init()
#mixer.music.load("back_music.ogg")
#mixer.music.play()
#fire_sound = mixer.Sound("")

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_a] and self.rect.x >= 10:
            self.rect.x -= self.speed

        if keys_pressed[K_d] and self.rect.x <= 625:
            self.rect.x += self.speed

        if keys_pressed[K_SPACE]:
            self.fire()
    
    def fire(self):
        #fire_sound.play()
        bullets.add(Bullet("laser.png",hero.rect.x,hero.rect.y-35, 15))

class Bullet(GameSprite):
    def update(self):    
        self.rect.y -= self.speed
        if self.rect.y == 0:
            self.kill

bullets = sprite.Group()


class Enemy(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(10,625)
            missed += 1
        self.speed = randint(1,5)

hero = Player("hero.png", window_width//2 , 400, 6)

enemies = sprite.Group()
for i in range(5):
    enemies.add(Enemy("enemy.png", randint(10,625),10, randint(0,5)))

clock = time.Clock()
game = True
finish = False
FPS = 60

font.init()


while game:
    if not finish:        
        window.blit(background, (0,0))

        hero.update()
        hero.reset()

        enemies.update()
        enemies.draw(window)
        
        bullets.update()
        bullets.draw(window)

        count_text = font.Font(None, 40).render(f"count: {count}", True, (224,224,224))
        missed_text = font.Font(None, 40).render(f"missed: {missed}", True, (224,224,224))

        window.blit(count_text,(10,10))
        window.blit(missed_text,(10,35))

    for e in event.get():
        if e.type == QUIT:
            game = False
    
    keys_pressed = key.get_pressed()
    if keys_pressed[K_SPACE]:
        hero.fire()

    display.update()
    clock.tick(FPS)
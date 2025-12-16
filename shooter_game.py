from pygame import *

from random import *
#background music
# mixer.init()
# mixer.music.load('fire.ogg')
# mixer.music.play()
#fire_sound = mixer.Sound('fire.ogg')



#fonts and caption
font.init()
font1 = font.SysFont('Gill Sans MT', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Gill Sans MT', 36)


#we need the following images:
img_back = "sea.jpg" # game background
img_hero = "rokety.png" # hero
img_enemy = "fishy.png" # enemy


score = 0 #ships destroyed
lost = 0 #ships missed
max_lost = 3
goal = 20

#parent class for other sprites
class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y, width, length, player_speed):
        super().__init__()
        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (width,length))
        self.speed = player_speed
        self.width = width
        self.length = length
        #every sprite must have the rect property - the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
#enemy sprite class
class Enemy(GameSprite):
    #enemy movement
    def update(self):
        self.rect.y += self.speed
        global lost
        #disappears upon reaching the screen edge
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

#bullet sprite class
class Bullet(GameSprite):
    #enemy movement
    def update(self):
        self.rect.y += self.speed
        #disappears upon reaching the screen edge
        if self.rect.y < 0:
            self.kill()


#create a window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


#create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)


bullets = sprite.Group()


#the "game is over" variable: as soon as True is there, sprites stop working in the main 
finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #fire_sound.play()
                ship.fire()


    if not finish:
        #update the background
        window.blit(background,(0,0))


        #write text on the screen
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))


        #launch sprite movements
        ship.update()
        monsters.update()
        bullets.update()


        #update them in a new location in each loop iteration
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)


        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #this loop will repeat as many times as the number of numbers hit
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        
        #possible lose: missed too many monsters or the character collided with
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True #lose, set the background and no longer control the s
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
            

        display.update()
    #the loop is expected each 0.05 sec
    
    time.delay(60)


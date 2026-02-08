from pygame import *
from random import randint
from time import \
    time as timer  # import the timing function so that the interpreter doesn’t need to look for this function in the pygame module time, give it a different name ourselves

# background music
mixer.init()
mixer.music.load('battle_music.ogg')
mixer.music.play()
fire_sound = mixer.Sound('juga_fire.ogg')

# fonts and labels
font.init()
font2 = font.Font(None, 36)

font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('omg kalah 0_0', True, (180, 0, 0))

# image
img_back = "grass.jpg"
img_hero = "shovel_thing_idk.png"
img_enemy = "idk_at_this_point_bro.png" # enemy :) :0 :(
img_bullet = "OMG_SOCIAL_INTERACTION_evaporates_lol_XD.png"

score = 0
lost = 0
max_lost = 3

goal = 10  # ini adalah goal yang kamu butuh tapi kamu tidak akan pernah tau karena ngak pernah akan menang :)

life = 3  # kalau abis yaa... matilah memang apa lagi woy


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    # silly kontrol untuk silly character :3
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 30, 35, -15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y < 0:
            self.kill()


# silly coding :3 :3
win_width = 700
win_height = 500
display.set_caption("Shooter Game Tapi Ngak Tau Lah - Hatta :)")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
    print('monster ke ', i, 'kecepatan = ', randint(1, 7))
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()
finish = False

# LOOPING???? NAHHHH >:(
run = True

rel_time = False  # LOL
num_fire = 0  # idk apa untuk dibilangin

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                # tembak suara
                # tembak

                # reload
                if num_fire < 10000 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 10000 and rel_time == False:  # if the player fired 8 shots
                    last_time = timer()  # moderator
                    rel_time = True  # no bullets?? :(

    if not finish:
        window.blit(background, (0, 0))

        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        if rel_time == True:
            now_time = timer()  # timer :/

            if now_time - last_time < 3:  # beep boop pow boom kablam!!!
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0  # no bullets? :( (2)
                rel_time = False  # same thing basically :/

        # IUSBGILSBNILVRBSLNVSIULVNHVIUSNHUNHKUDHLVNISUNHVISJDOFJIOSJ
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # SOCIAL INTERACTION???? *evaporates*
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        # :)
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True  # :0
            window.blit(lose, (200, 200))

        # :D
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        display.update()
    time.delay(50)

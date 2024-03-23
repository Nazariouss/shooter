#Створи власний Шутер!
from pygame import *
from random import randint

mixer.init()
# mixer.music.load("space.ogg")
# mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

font.init()
font0 = font.Font(None, 36)
font1 = font.Font(None, 80)

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

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

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        #створюємо об'єкти кулі
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 10, 30, -10)
        #додаємо кулю до групи
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        #рух кулі до верхньої межі екрану і зникання
        self.rect.y += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.y < 0:
            self.kill()

bullets = sprite.Group()

monsters = sprite.Group()
for i in range(5):
    monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
lost = 0
max_lost = 3
goal = 10
score = 0
clock = time.Clock()

finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                # fire_sound.play()
                ship.fire()


    if not finish:
        window.blit(background, (0,0))
        ship.update()
        ship.reset()

        text = font0.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font0.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        monsters.draw(window)
        monsters.update()

        #відмальовка та рух куль
        bullets.draw(window)
        bullets.update()

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            lose = font1.render("YOU LOSE", True, (255, 255, 255))
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            win = font1.render("YOU WIN!", True, (255, 255, 255))
            window.blit(win, (200, 200))

        display.update()

    clock.tick(60)
    


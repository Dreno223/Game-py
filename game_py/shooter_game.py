
from random import randint
from pygame import *
from time import time as timer
class GameSprite(sprite.Sprite):
	def __init__(self,player_image,player_x,player_y,size_x,size_y,speed):
		#super().__init__()
		sprite.Sprite.__init__(self)
		self.image = transform.scale(image.load(player_image),(size_x,size_y))
		self.speed = speed

		self.rect = self.image.get_rect()
		self.rect.x = player_x
		self.rect.y = player_y
		self.life = 3

	def reset(self):
		window.blit(self.image,(self.rect.x,self.rect.y))


class Player(GameSprite):
	def update(self):
		keys = key.get_pressed()

		if keys[K_a] and self.rect.x > 5:
			self.rect.x -= self.speed
		if keys[K_d] and self.rect.x < win_width - 80:
			self.rect.x += self.speed
	def fire(self):
		bullet = Bullet("bullet1.png",self.rect.centerx-5,self.rect.top,15,20,10)
		bullets.add(bullet)

class Enemy(GameSprite):

	def update(self):
		self.rect.y += self.speed
		global miss
		if self.rect.y>700:
			self.rect.y = -70
			self.rect.x = randint(80,1200)
			miss+=1

class Asteroid(GameSprite):

	def update(self):
		self.rect.y += self.speed
		global miss
		if self.rect.y>700:
			self.rect.y = -70
			self.rect.x = randint(80,1200)
			

class Bullet(GameSprite):
	
	def update (self):
		self.rect.y -= self.speed
		if self.rect.y<0:
			self.kill


asteroids = sprite.Group()
for x in range(2):
	asteroid = Asteroid("asteroid.png",randint(80,1200),-40,80,120,randint(1,7))
	asteroids.add(asteroid)

bullets = sprite.Group()
win_width = 1280
win_height = 693
window = display.set_mode((win_width, win_height))
display.set_caption("pewpew")
background = transform.scale(image.load("galaxy1.jpg"), (win_width, win_height))

ship = Player("spaceship.png",640,580,80,100,10)
enemys = sprite.Group()

for i in range(5):
	enemy = Enemy("enemy.png",randint(80,1200),-40,80,100,randint(1,3))
	enemys.add(enemy)

mixer.init()
mixer.music.load('Married life.mp3')
mixer.music.play()
fire = mixer.Sound('gun.wav')

font.init()

font1 = font.Font(None,120)
win = font1.render("Victory!", True,(255,255,255))
lose = font1.render("Defeat", True,(255,255,255))
font2 = font.Font(None,36)


miss = 0
score = 0
finish = 0

finish = False
run = True
clock = time.Clock()

rel_time = False
num_fire = 0
while run:
	for e in event.get():

		if e.type == QUIT:
			run = False

		elif e.type == KEYDOWN:
			if e.key == K_SPACE and finish == False:
				if num_fire<5 and rel_time == False:
					fire.play()
					ship.fire()
					num_fire+=1

				if num_fire>=5 and rel_time == False:
					last_time = timer()
					rel_timer = True

		elif e.type == MOUSEBUTTONDOWN and finish == False:
			if e.button == 1:
				if num_fire<5 and rel_time == False:
					fire.play()
					ship.fire()  
					num_fire+=1
				if num_fire>=5 and rel_time == False:
					last_time = timer()
					rel_timer = True
					

	if not finish:
		window.blit(background,(0,0))
		if rel_time == True:
			now_time = timer()
			if now_time - last_time<1:
				reloading - font2.render("wait, reading",1,(150,0,0))
				window.blit(reloading,(260,460))
		sprites_list = sprite.spritecollide(ship, enemys, False)
		
		if sprites_list or miss >= 3 or ship.life<1:
			finish = True
			window.blit(lose,(500,100))
		
		sprite_asteroid = sprite.spritecollide(ship,asteroids,True)
		if sprite_asteroid:
			ship.life -= 1 
			asteroid = Asteroid("asteroid.png",randint(80,1200),-40,80,120,randint(1,7))
		collides = sprite.groupcollide(enemys,bullets,True,True)
		
		for c in collides:
			score = score+1
			enemy = Enemy("enemy.png", randint(80,1200),-40,80,100,randint(1,3))
			enemys.add(enemy)
		
		if score >= 30:
			finish = True
			window.blit(win,(500,100))
		
		text = font2.render("Score:" +str(score),1,(255,255,255))
		window.blit(text,(10,10))
		text_lose = font2.render("Missed: "+str(miss),1,(255,255,255))
		window.blit(text_lose,(10,40))
		text_life = font2.render("Lives: "+str(ship.life),1,(255,255,255))
		window.blit(text_life,(10,70))

		bullets.update()
		bullets.draw(window)
		ship.update()
		ship.reset()
		enemys.update()
		enemys.draw(window)
		asteroids.update()
		asteroids.draw(window)

		display.update()
	else:
		finsih = False
		score = 0
		lost = 0
		ship.life = 3
		for b in bullets:
			b.kill()
		for m in enemys:
			m.kill()

		time.delay(3000)
		for i in range(5):
			enemy = Enemy("enemy.png",randint(80,1200),-40,80,100,randint(1,3))
			enemys.add(enemy)
	clock.tick(100)
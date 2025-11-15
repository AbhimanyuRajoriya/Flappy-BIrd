import pygame as pg
import sys
import time
from bird import birdie
from pipe import Pipe
pg.init()

class game:
    def __init__(self):
        self.width = 600
        self.hight = 768
        pg.display.set_caption("Flappy Bird")
        self.scale_factor = 1.5
        self.win = pg.display.set_mode((self.width, self.hight))
        self.clock = pg.time.Clock()
        self.move_speed = 200

        pg.mixer.music.load("asset/sfx/bgM.mp3")
        pg.mixer.music.set_volume(0.10)
        pg.mixer.music.play(-1) 
        self.clk = pg.mixer.Sound("asset/sfx/flap.wav")
        self.dead = pg.mixer.Sound("asset/sfx/dead.wav")
        self.played_hit_sound = False

        self.monitoring = False
        self.score = 0
        self.font = pg.font.Font("asset/font.ttf",24)
        self.scoreFont = self.font.render("Score: 0 ", True, (255,255,255))
        self.score_rec = self.scoreFont.get_rect(center = (100, 30))
        
        self.Restart = self.font.render("Restart", True, (0,0,0))
        self.Restart_rect = self.Restart.get_rect(center = (300, 650))

        self.bird = birdie(self.scale_factor)
        self.is_gameStrd = True
        self.isentPressed = False
        self.pipes = []
        self.pipe_gen = 71
        self.setup()

        self.gameloop()

    def setup(self):
        self.bg_img = pg.transform.scale_by(pg.image.load("asset/bg.png").convert(), self.scale_factor)

        self.ground1_img = pg.transform.scale_by(pg.image.load("asset/ground.png").convert(), self.scale_factor)
        self.ground2_img = pg.transform.scale_by(pg.image.load("asset/ground.png").convert(), self.scale_factor)

        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()

        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.ground1_rect.y = 568
        self.ground2_rect.y = 568

    def gameloop(self):
        last_time = time.time()
        while True:
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and self.is_gameStrd:
                    self.clk.play()
                    self.isentPressed = True
                    self.bird.updtON= True
                    self.bird.fly(dt)
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.Restart_rect.collidepoint(pg.mouse.get_pos()):
                        self.restartGame()

            self.updGround(dt)
            self.collision()
            self.setscore()
            self.drawE()
            pg.display.update()
            self.clock.tick(60)

    def updGround(self, dt):
        if self.isentPressed:
            self.ground1_rect.x -= self.move_speed * dt
            self.ground2_rect.x -= self.move_speed * dt

            if self.ground1_rect.right < 0:
                self.ground1_rect.x = self.ground2_rect.right
            if self.ground2_rect.right < 0:
                self.ground2_rect.x = self.ground1_rect.right

            if self.pipe_gen > 100:
                self.pipes.append(Pipe(self.scale_factor, self.move_speed))
                self.pipe_gen = 0
            self.pipe_gen += 1

            for pipe in self.pipes:
                pipe.update(dt)

            if len(self.pipes)!=0:
                if self.pipes[0].rect_up.right <0:
                    self.pipes.pop(0)
        self.bird.update(dt)
        
    def drawE(self):
        self.win.blit(self.bg_img, (0, -300))
        for pipe in self.pipes:
            pipe.drawPipe(self.win)
        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)
        self.win.blit(self.bird.image, self.bird.rect)
        self.win.blit(self.scoreFont, self.score_rec)
        if not self.is_gameStrd:
            self.win.blit(self.Restart, self.Restart_rect)

    def setscore(self):
        if len(self.pipes)>0:
            if (self.bird.rect.left > self.pipes[0].rect_down.left and self.bird.rect.right < self.pipes[0].rect_down.right and not self.monitoring):
                self.monitoring = True

            if (self.bird.rect.left > self.pipes[0].rect_down.right and self.monitoring):
                self.score +=1
                self.scoreFont = self.font.render(f"Score: {self.score} ", True, (255,255,255))
                self.monitoring = False

    def collision(self):
        if len(self.pipes):
            if self.bird.rect.bottom>568:
                if not self.played_hit_sound:
                    self.dead.play()
                    self.played_hit_sound= True
                self.bird.updtON = False
                self.isentPressed = False
                self.is_gameStrd = False
            if(self.bird.rect.colliderect(self.pipes[0].rect_down) or self.bird.rect.colliderect(self.pipes[0].rect_up)):
                if not self.played_hit_sound:
                    self.dead.play()
                    self.played_hit_sound= True
                self.bird.updtON = False
                self.bird.velocity = 0
                self.isentPressed = False
                self.is_gameStrd = False

    def restartGame(self):
        self.score = 0
        self.scoreFont = self.font.render("Score: 0 ", True, (255,255,255))
        self.isentPressed = False
        self.is_gameStrd = True
        self.bird.resBird()
        self.pipes.clear()
        self.played_hit_sound = False 
g = game()
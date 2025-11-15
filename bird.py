import pygame as pg

class birdie(pg.sprite.Sprite):
    def __init__(self, scale_factor):
        super(birdie, self).__init__()
        self.img_list = [pg.transform.scale_by(pg.image.load("asset/birdup.png").convert_alpha(), scale_factor),
                         pg.transform.scale_by(pg.image.load("asset/birdmid.png").convert_alpha(), scale_factor),
                         pg.transform.scale_by(pg.image.load("asset/birddown.png").convert_alpha(), scale_factor)]
        self.imageidx = 0
        self.image = self.img_list[self.imageidx]
        self.rect = self.image.get_rect(center = (100, 300))
        self.velocity = 0
        self.gravity = 10
        self.flap_speed = 275
        self.counter =0 
        self.updtON = False

    def update(self, dt):
        if not self.updtON:
            return
        self.anime()
        self.grav(dt)

        if self.rect.y < 0:
            self.rect.y = 0
            self.velocity = 0


    def grav(self, dt):
        self.velocity += self.gravity*dt
        self.rect.y +=self.velocity

    def fly(self, dt):
        self.velocity = -self.flap_speed*dt

    def anime(self):
        if self.counter==5:
            self.image = self.img_list[self.imageidx]
            if self.imageidx == 0 : self.imageidx =1
            else : self.imageidx = 0
            self.counter = 0
        self.counter+=1

    def resBird(self):
        self.rect.center=(100,300)
        self.velocity = 0
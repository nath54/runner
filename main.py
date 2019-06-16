#coding:utf-8
import random,pygame,time
from pygame.locals import *

pygame.init()

btex,btey=700,500
tex,tey=700,500

fenetre=pygame.display.set_mode([tex,tey])
pygame.display.set_caption("runner")
pygame.key.set_repeat(40,30)

def rx(x): return int(x/btex*tex)
def ry(y): return int(y/btey*tey)

font=pygame.font.SysFont("Serif",ry(15))

dimgs="images/"
panims=[["p1-1.png","p1-2.png","p1-3.png","p1-4.png","p1-5.png","p1-6.png","p1-7.png""p1-8.png"]]

imgsbackgrounds=[]
imgbg=pygame.transform.scale(pygame.image.load(random.choice(imgsbackgrounds)),[tex*2,tey])

class Perso:
    def __init__(self,nom,tpi,ks):
        self.nom=nom
        self.tx,self.ty=rx(100),ry(100)
        self.px=random.randint(self.tx,tex-self.tx)
        self.py=random.randint(self.tx,tey-self.ty)
        self.keyup=ks[0]
        self.keydown=ks[1]
        self.keyleft=ks[2]
        self.keyright=ks[3]
        self.vit=rx(15)
        self.db=time.time()
        self.tb=0.01
        self.imgs=[]
        for i in panims[tpi]: imgs.append( pygame.transform.scale(pygame.image.load(dimgs+i),[self.tx,self.ty])
        self.an=0
        self.image=self.imgs[self.an]
        self.dan=time.time()
        self.tan=0.1
        self.vie=3
        self.tpinv=0
        self.dinv=time.time()
        self.dclign=time.time()
        self.tclign=0.2
        self.isclign=False
    def bouger(self,aa):
        if time.time()-self.db >= self.tb:
            self.db=time.time()
            if aa=="up":
                self.py-=self.vit
                if self.py < self.ty: self.py=self.ty
            elif aa=="down":
                self.py+=self.vit
                if self.py > tey-self.ty: self.py=tey-self.ty
            elif aa=="left":
                self.px-=self.vit
                if self.px < self.tx: self.px=self.tx
            elif aa=="right":
                self.px+=self.vit
                if self.px > tex-self.tx: self.px=tex-self.tx
    def anim(self):
        if time.time()-self.dan >= self.tan:
            self.dan=time.time()
            self.an+=1
            if self.an>=len(self.imgs): self.an=0
            self.image=self.imgs[self.an]
        if tpinv>0:
            if time.time()-self.dclign >= self.tclign:
                self.dclign=time.time()
                self.isclign=not isclign

def verif_keys(persos):
    keys=pygame.key.get_pressed()
    for p in persos:
        if keys[p.keyup]:  p.bouger("up")
        if keys[p.keydown]:  p.bouger("down")
        if keys[p.keyleft]:  p.bouger("left")
        if keys[p.keyright]:  p.bouger("right")
    
def aff(persos,obstacles,fps):
    fenetre.fill((0,0,0))
    for p in persos:
        if p.tpinv <= 0: fenetre.blit(p.img,[p.px,p.py])
        else:
            if not p.isclign: fenetre.blit(p.img,[p.px,p.py])
        fenetre.blit(font.render(p.nom,20,p.cl),[p.px,p.py-ry(15)])
    fenetre.blit(font.render("fps : "+fps,20,(255,255,255)),[rx(15),ry(15)])
    pygame.display.update()

obstacles=[]
persos=[]
fps=0
encour=True
while encour:
    t1=time.time()
    for p in persos: p.anim()
    verif_keys(persos)
    aff(persos,obstacles)
    for event in pygame.event.get():
        if event.type==QUIT: exit()
        elif event.type==KEYDOWN:
            if event.key==K_ESCAPE: encour=False
    t2=time.time()
    fps=str(int(1./(t2-t1)))
            


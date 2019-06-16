#coding:utf-8
import random,pygame,time
from pygame.locals import *

pygame.init()

btex,btey=700,500
btx,bty=1280,1024

io = pygame.display.Info() #on récurpère dans la variable io les infos sur l'affichage de l'utilisateur
mtex,mtey=io.current_w,io.current_h #on assigne à mtex et mtey la taille actuelle de l'ecran de l'ordinateur
tex,tey=int(btex/btx*mtex),int(btey/bty*mtey) #avec les données ci-dessus on calcule la taille de la fenetre du jeu pour qu'elle soit adaptée à l'écran de l'utilisateur


fenetre=pygame.display.set_mode([tex,tey])
pygame.display.set_caption("runner")
pygame.key.set_repeat(40,30)

def rx(x): return int(x/btex*tex)
def ry(y): return int(y/btey*tey)

font=pygame.font.SysFont("Serif",ry(15))
font2=pygame.font.SysFont("Serif",ry(22))

dimgs="images/"
tpanims=[["p1-1.png","p1-2.png","p1-3.png","p1-4.png","p1-5.png","p1-6.png","p1-7.png","p1-8.png"],["p2-1.png","p2-2.png","p2-3.png","p2-4.png","p2-5.png","p2-6.png","p2-7.png","p2-8.png"],["p3-1.png","p3-2.png","p3-3.png","p3-4.png","p3-5.png","p3-6.png","p3-7.png","p3-8.png"],["p4-1.png","p4-2.png","p4-3.png","p4-4.png","p4-5.png","p4-6.png","p4-7.png","p4-8.png","p4-9.png","p4-10.png","p4-11.png","p4-12.png","p4-13.png","p4-14.png","p4-15.png","p4-16.png"]]

imgsbackgrounds=["bg1.png"]
imgcoeur=pygame.transform.scale(pygame.image.load(dimgs+"coeur.png"),[rx(25),ry(25)])

tpobs=[["baril","o1.png",rx(34),ry(47),True]]
#0=nom , 1=img , 2=tx , 3=ty , 4=kill(True or False)

class Obstacle:
    def __init__(self,x,y,tp):
        self.nom=tpobs[tp][0]
        self.px=x
        self.py=y
        self.tx=tpobs[tp][2]
        self.ty=tpobs[tp][3]
        self.kill=tpobs[tp][4]
        self.img=pygame.transform.scale(pygame.image.load(dimgs+tpobs[tp][1]),[self.tx,self.ty])
        self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
        self.delete=False

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
        for i in tpanims[tpi]: self.imgs.append( pygame.transform.scale(pygame.image.load(dimgs+i),[self.tx,self.ty]) )
        self.an=0
        self.img=self.imgs[self.an]
        self.dan=time.time()
        self.tan=0.1
        self.vie=3
        self.tpinv=3
        self.dinv=time.time()
        self.dclign=time.time()
        self.tclign=0.2
        self.isclign=False
        self.cl=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.rect=pygame.Rect(self.px,self.py,self.tx,self.ty)
        self.score=0
        self.tdeb=time.time()
        self.tfin=0
    def bouger(self,aa):
        if time.time()-self.db >= self.tb:
            self.db=time.time()
            if aa=="up":
                self.py-=self.vit
                if self.py < 0: self.py=0
            elif aa=="down":
                self.py+=self.vit
                if self.py > tey-self.ty: self.py=tey-self.ty
            elif aa=="left":
                self.px-=self.vit
                if self.px < 0: self.px=0
            elif aa=="right":
                self.px+=self.vit
                if self.px > tex-self.tx: self.px=tex-self.tx
    def anim(self):
        if time.time()-self.dan >= self.tan:
            self.dan=time.time()
            self.an+=1
            if self.an>=len(self.imgs): self.an=0
            self.img=self.imgs[self.an]
        if self.tpinv>0:
            if time.time()-self.dclign >= self.tclign:
                self.dclign=time.time()
                self.isclign=not self.isclign
            self.tpinv-=time.time()-self.dinv
            self.dinv=time.time()

def gameloop(obstacles,bgx1,bgx2,vit,nbobs,davit,tavit,persos,tno,dno,tmv,dmv):
    while len(obstacles)<nbobs: obstacles.append( Obstacle(random.randint(tex,tex*2),random.randint(0,tey),random.randint(0,len(tpobs)-1)) )
    if time.time()-dmv>=tmv:
        dmv=time.time()
        for o in obstacles:
            for p in persos:
                if p.vie>0 and p.tpinv<=0 and o.rect.colliderect(p.rect):
                    p.vie-=1
                    p.tpinv=3
                    p.dinv=time.time()
                    p.px,p.py=random.randint(p.tx,tex-p.tx),random.randint(p.ty,tey-p.ty)
                    p.score-=1000
                    if p.vie<=0:
                        p.tfin=time.time()
                    o.delete=True
            o.px-=rx(vit)
            if o.px+o.tx <= 0:
                o.delete=True
        for o in obstacles:
            if o.delete:
                if o in obstacles : del(obstacles[obstacles.index(o)])
        bgx1-=rx(vit)
        bgx2-=rx(vit)
        if bgx1<=-tex: bgx1=tex-rx(vit)
        if bgx2<=-tex: bgx2=tex-rx(vit)
        for p in persos:
            if p.vie>0: p.score+=rx(vit)
    if time.time()-davit >= tavit:
        if vit<50: vit+=0.5
        davit=time.time()
        if tavit > 1 : tavit-=0.05
    if time.time()-dno>=tno and nbobs<15:
        dno=time.time()
        nbobs+=1
    return tavit,davit,bgx1,bgx2,obstacles,vit,persos,tno,dno,nbobs,dmv

def verif_keys(persos):
    keys=pygame.key.get_pressed()
    for p in persos:
        if keys[p.keyup]:  p.bouger("up")
        if keys[p.keydown]:  p.bouger("down")
        if keys[p.keyleft]:  p.bouger("left")
        if keys[p.keyright]:  p.bouger("right")
    
def aff(persos,obstacles,fps,imgbg1,imgbg2,bgx1,bgx2,vit,nbobs):
    fenetre.fill((0,0,0))
    fenetre.blit(imgbg1,[bgx1,0])
    fenetre.blit(imgbg2,[bgx2,0])
    fenetre.blit( font.render("speed : "+str(vit),20,(250,0,0)) , [rx(15),ry(425)])
    fenetre.blit( font.render("nb obstacle : "+str(nbobs),20,(250,0,0)) , [rx(15),ry(450)])
    xx,yy=15,30
    for p in persos:
        fenetre.blit(font.render(p.nom+" score : "+str(p.score),20,p.cl),[rx(xx),ry(yy)])
        if p.vie>0:
            for w in range(p.vie):
                fenetre.blit(imgcoeur,[rx(xx+w*25),ry(yy+15)])
        yy+=50
        if p.vie>0:
            if p.tpinv <= 0: p.rect=fenetre.blit(p.img,[p.px,p.py])
            else:
                if not p.isclign: fenetre.blit(p.img,[p.px,p.py])
            fenetre.blit(font.render(p.nom,20,p.cl),[p.px,p.py-ry(15)])
    for o in obstacles: o.rect=fenetre.blit(o.img,[o.px,o.py])
    fenetre.blit(font.render("fps : "+str(fps),20,(255,255,255)),[rx(15),ry(15)])
    pygame.display.update()

def main_jeu():
    imgbg1=pygame.transform.scale(pygame.image.load(dimgs+random.choice(imgsbackgrounds)),[tex+100,tey])
    imgbg2=pygame.transform.scale(pygame.image.load(dimgs+random.choice(imgsbackgrounds)),[tex+100,tey])
    bgx1=0
    bgx2=bgx1+tex
    vit=5
    nbobs=1
    obstacles=[]
    persos=[]
    fps=0
    davit=time.time()
    tavit=10.0
    tno=5
    dno=time.time()
    persos.append( Perso("player1",random.randint(0,len(tpanims)-1),[K_UP,K_DOWN,K_LEFT,K_RIGHT]) )
    persos.append( Perso("player2",random.randint(0,len(tpanims)-1),[K_i,K_k,K_j,K_l]) )
    persos.append( Perso("player3",random.randint(0,len(tpanims)-1),[K_e,K_d,K_s,K_f]) )
    persos.append( Perso("player4",random.randint(0,len(tpanims)-1),[K_KP8,K_KP2,K_KP4,K_KP6]) )
    encour=True
    nbviv=len(persos)
    perdu=False
    dmv=time.time()
    tmv=0.001
    while encour:
        t1=time.time()
        for p in persos:
            if p.vie>0: p.anim()
        verif_keys(persos)
        tavit,davit,bgx1,bgx2,obstacles,vit,persos,tno,dno,nbobs,dmv=gameloop(obstacles,bgx1,bgx2,vit,nbobs,davit,tavit,persos,tno,dno,tmv,dmv)
        aff(persos,obstacles,fps,imgbg1,imgbg2,bgx1,bgx2,vit,nbobs)
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE: encour=False
        nbviv=0
        for p in persos:
            if p.vie>0: nbviv+=1
        if nbviv==0:    
            encour=False
            perdu=True
        t2=time.time()
        fps=int(1./(t2-t1))
    if perdu:
        fenetre.fill((100,200,150))
        clas=[]
        while len(clas)<len(persos):
            lpp=0
            while persos[lpp] in clas: lpp+=1
            for p in persos:
                if not p in clas:
                    if p.score >= persos[lpp].score: lpp=persos.index(p)
            clas.append(persos[lpp])
        pos=1
        xx,yy=150,50
        for p in clas:
            fenetre.blit( font2.render(str(pos)+" : "+p.nom+" - "+str(p.score)+" - "+str(int(p.tfin-p.tdeb))+" sec",20,(255,255,255)) , [rx(xx),ry(yy)])
            fenetre.blit( pygame.transform.scale(p.img,[rx(50),ry(50)]) , [rx(xx-70),ry(yy)])
            yy+=50
            pos+=1
        fenetre.blit(font2.render("END",20,(255,50,50)),[rx(200),ry(10)])
        fenetre.blit(font2.render("Press SPACE to continue",20,(20,150,50)),[rx(200),ry(300)])
        pygame.display.update()
        encoure=True
        while encoure:
            for event in pygame.event.get():
                if event.type==QUIT: exit()
                elif event.type==KEYDOWN:
                    if event.key==K_ESCAPE: encoure=False
                    elif event.key==K_SPACE: encoure=False
                    
        
main_jeu()

                

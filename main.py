#coding:utf-8
#!/bin/python3
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
tpanims=[["p1-1.png","p1-2.png","p1-3.png","p1-4.png","p1-5.png","p1-6.png","p1-7.png","p1-8.png"],["p2-1.png","p2-2.png","p2-3.png","p2-4.png","p2-5.png","p2-6.png","p2-7.png","p2-8.png"],["p3-1.png","p3-2.png","p3-3.png","p3-4.png","p3-5.png","p3-6.png","p3-7.png","p3-8.png"],["p4-1.png","p4-2.png","p4-3.png","p4-4.png","p4-5.png","p4-6.png","p4-7.png","p4-8.png","p4-9.png","p4-10.png","p4-11.png","p4-12.png","p4-13.png","p4-14.png","p4-15.png","p4-16.png"],["p5-1.png","p5-2.png","p5-3.png","p5-4.png","p5-5.png","p5-6.png","p5-7.png","p5-8.png"]]

animspersos=[]

for an in tpanims:
    animspersos.append([])
    for im in an: animspersos[tpanims.index(an)].append( pygame.transform.scale(pygame.image.load(dimgs+im),[rx(75),ry(75)]) )

imgrandommenu=pygame.transform.scale(pygame.image.load(dimgs+"random.png"),[rx(75),ry(75)])
imgkp1=pygame.transform.scale(pygame.image.load(dimgs+"keysp1.png"),[rx(125),ry(80)])
imgkp2=pygame.transform.scale(pygame.image.load(dimgs+"keysp2.png"),[rx(125),ry(80)])
imgkp3=pygame.transform.scale(pygame.image.load(dimgs+"keysp3.png"),[rx(125),ry(80)])
imgkp4=pygame.transform.scale(pygame.image.load(dimgs+"keysp4.png"),[rx(125),ry(80)])

imgsbackgrounds=["bg1.png"]
imgcoeur=pygame.transform.scale(pygame.image.load(dimgs+"coeur.png"),[rx(25),ry(25)])

tpobs=[["baril","o1.png",rx(34),ry(47),True],["plant1","o2.png",rx(81),ry(57),False],["plant2","o3.png",rx(38),ry(26),False]]
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
    def __init__(self,nom,tpi,ks,bot):
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
        self.vie=3
        self.tpinv=3
        self.dinv=time.time()
        self.dclign=time.time()
        self.tclign=0.2
        self.isclign=False
        self.cl=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.rect=pygame.Rect(self.px,self.py+self.ty/2,self.tx,self.ty/2)
        self.score=0
        self.tdeb=time.time()
        self.tfin=0
        self.bot=bot
        self.dbouger=time.time()
        self.tbouger=0.05
        self.dmov=None
    def bouger(self,aa):
        if time.time()-self.db >= self.tb:
            self.db=time.time()
            if aa=="up":
                self.dmov=aa
                self.py-=self.vit
                if self.py < 0: self.py=0
            elif aa=="down":
                self.dmov=aa
                self.py+=self.vit
                if self.py > tey-self.ty: self.py=tey-self.ty
            elif aa=="left":
                self.dmov=aa
                self.px-=self.vit
                if self.px < 0: self.px=0
            elif aa=="right":
                self.dmov=aa
                self.px+=self.vit
                if self.px > tex-self.tx: self.px=tex-self.tx
    def anim(self,tpan):
        if time.time()-self.dan >= tpan:
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

def gameloop(obstacles,bgx1,bgx2,vit,nbobs,davit,tavit,persos,tno,dno,tmv,dmv,tpan):
    while len(obstacles)<nbobs: obstacles.append( Obstacle(random.randint(tex,tex*2),random.randint(0,tey),random.randint(0,len(tpobs)-1)) )
    if time.time()-dmv>=tmv:
        dmv=time.time()
        for o in obstacles:
            for p in persos:
                if o.kill and p.vie>0 and p.tpinv<=0 and o.rect.colliderect(pygame.Rect(p.px,p.py+p.ty/2,p.tx,p.ty/2)):
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
        if tpan > 0.01: tpan-=0.001
    if time.time()-dno>=tno and nbobs<15:
        dno=time.time()
        nbobs+=1
    return tavit,davit,bgx1,bgx2,obstacles,vit,persos,tno,dno,nbobs,dmv,tpan

def verif_keys(persos):
    keys=pygame.key.get_pressed()
    for p in persos:
        if not p.bot:
            if keys[p.keyup]:  p.bouger("up")
            if keys[p.keydown]:  p.bouger("down")
            if keys[p.keyleft]:  p.bouger("left")
            if keys[p.keyright]:  p.bouger("right")

def bot(p,obs,vit):
    if True:
        lstmov=["up","down","left","right",None]
        for x in range(10): lstmov.append(p.dmov)
        if p.dmov!=None : p.bouger(random.choice(lstmov))
        for o in obs:
            if o.kill:
                ofr=pygame.Rect(0,o.py,tex,o.ty)
                if ofr.colliderect(pygame.Rect(p.px,p.py+p.ty,p.tx,p.ty)):
                    direc=random.choice(["up","down"])
                    p.bouger(random.choice([direc]))
            

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

def main_jeu(p1,p2,p3,p4):
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
    tpan=0.1
    dno=time.time()
    if p1[0]==-1: p1[0]=random.randint(0,len(tpanims)-1)
    if p2[0]==-1: p2[0]=random.randint(0,len(tpanims)-1)
    if p3[0]==-1: p3[0]=random.randint(0,len(tpanims)-1)
    if p4[0]==-1: p4[0]=random.randint(0,len(tpanims)-1)    
    if p1[0]!=None : persos.append( Perso(p1[1],p1[0],p1[2],p1[3]) )
    if p2[0]!=None : persos.append( Perso(p2[1],p2[0],p2[2],p2[3]) )
    if p3[0]!=None : persos.append( Perso(p3[1],p3[0],p3[2],p3[3]) )
    if p4[0]!=None : persos.append( Perso(p4[1],p4[0],p4[2],p4[3]) )
    encour=True
    nbviv=len(persos)
    perdu=False
    dmv=time.time()
    tmv=0.001
    while encour:
        t1=time.time()
        for p in persos:
            if p.vie>0: p.anim(tpan)
            if p.bot: bot(p,obstacles,vit)
        verif_keys(persos)
        tavit,davit,bgx1,bgx2,obstacles,vit,persos,tno,dno,nbobs,dmv,tpan=gameloop(obstacles,bgx1,bgx2,vit,nbobs,davit,tavit,persos,tno,dno,tmv,dmv,tpan)
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

def aff_menu(p1,p2,p3,p4,fps):
    fenetre.fill((0,0,0))
    bts=[]
    for x in range(9): bts.append(None)
    #p1
    p1x,p1y=75,75
    bts[1]=pygame.draw.rect(fenetre,(90,90,90),(rx(p1x),ry(p1y),rx(75),ry(75)),0)
    if p1[0]!=None:
        if p1[0]!=-1: fenetre.blit(animspersos[p1[0]][p1[4]],[rx(p1x),ry(p1y)])
        else: fenetre.blit(imgrandommenu,[rx(p1x),ry(p1y)])
        fenetre.blit(font2.render(p1[1],20,(255,255,255)),[rx(p1x),ry(p1y-30)])
        bts[2]=pygame.draw.rect(fenetre,(0,20,120),(rx(p1x-20),ry(p1y+120),rx(100),ry(35)),0)
        if p1[3]: p1txt=font.render("bot",20,(255,255,255))
        else: p1txt=font.render("human",20,(255,255,255))
        fenetre.blit( p1txt , [rx(p1x),ry(p1y+125)] )
        fenetre.blit( imgkp1 , [rx(p1x-50),ry(p1y+200)] )
    else: fenetre.blit( font.render("None",20,(250,250,250)) , [rx(p1x+15),ry(p1y)+30] )
    #p2
    p2x,p2y=75+150,75
    bts[3]=pygame.draw.rect(fenetre,(90,90,90),(rx(p2x),ry(p2y),rx(75),ry(75)),0)
    if p2[0]!=None:
        if p2[0]!=-1: fenetre.blit(animspersos[p2[0]][p2[4]],[rx(p2x),ry(p2y)])
        else: fenetre.blit(imgrandommenu,[rx(p2x),ry(p2y)])
        fenetre.blit(font2.render(p2[1],20,(255,255,255)),[rx(p2x),ry(p2y-30)])
        bts[4]=pygame.draw.rect(fenetre,(0,20,120),(rx(p2x-20),ry(p2y+120),rx(100),ry(35)),0)
        if p2[3]: p2txt=font.render("bot",20,(255,255,255))
        else: p2txt=font.render("human",20,(255,255,255))
        fenetre.blit( p2txt , [rx(p2x),ry(p2y+125)] )
        fenetre.blit( imgkp2 , [rx(p2x-50),ry(p2y+200)] )
    else: fenetre.blit( font.render("None",20,(250,250,250)) , [rx(p2x+15),ry(p2y)+30] )
    #p2
    p3x,p3y=75+300,75
    bts[5]=pygame.draw.rect(fenetre,(90,90,90),(rx(p3x),ry(p3y),rx(75),ry(75)),0)
    if p3[0]!=None:
        if p3[0]!=-1: fenetre.blit(animspersos[p3[0]][p3[4]],[rx(p3x),ry(p3y)])
        else: fenetre.blit(imgrandommenu,[rx(p3x),ry(p3y)])
        fenetre.blit(font2.render(p3[1],20,(255,255,255)),[rx(p3x),ry(p3y-30)])
        bts[6]=pygame.draw.rect(fenetre,(0,20,120),(rx(p3x-20),ry(p3y+120),rx(100),ry(35)),0)
        if p3[3]: p3txt=font.render("bot",20,(255,255,255))
        else: p3txt=font.render("human",20,(255,255,255))
        fenetre.blit( p3txt , [rx(p3x),ry(p3y+125)] )
        fenetre.blit( imgkp3 , [rx(p3x-50),ry(p3y+200)] )
    else: fenetre.blit( font.render("None",20,(250,250,250)) , [rx(p3x+15),ry(p3y)+30] )
    #p4
    p4x,p4y=75+450,75
    bts[7]=pygame.draw.rect(fenetre,(90,90,90),(rx(p4x),ry(p4y),rx(75),ry(75)),0)
    if p4[0]!=None:
        if p4[0]!=-1: fenetre.blit(animspersos[p4[0]][p4[4]],[rx(p4x),ry(p4y)])
        else: fenetre.blit(imgrandommenu,[rx(p4x),ry(p4y)])
        fenetre.blit(font2.render(p4[1],20,(255,255,255)),[rx(p4x),ry(p4y-30)])
        bts[8]=pygame.draw.rect(fenetre,(0,20,120),(rx(p4x-20),ry(p4y+120),rx(100),ry(35)),0)
        if p4[3]: p4txt=font.render("bot",20,(255,255,255))
        else: p4txt=font.render("human",20,(255,255,255))
        fenetre.blit( p4txt , [rx(p4x),ry(p4y+125)] )
        fenetre.blit( imgkp4 , [rx(p4x-50),ry(p4y+200)] )
    else: fenetre.blit( font.render("None",20,(250,250,250)) , [rx(p4x+15),ry(p4y)+30] )
    #0
    bts[0]=pygame.draw.rect(fenetre,(151,150,0),(rx(285),ry(400),rx(150),ry(75)),0)
    fenetre.blit( font.render("Play !",20,(0,0,0)) , [rx(325),ry(410)] )
    fenetre.blit( font2.render("Runner",20,(250,0,0)) , [rx(325),ry(5)] )
    fenetre.blit( font.render("fps : "+str(fps),20,(255,255,255)) ,[rx(10),ry(10)] )
    pygame.display.update()
    return bts

def main_menu():
    tpan=0.1
    dani=time.time()
    p1=[None,"player1",[K_UP,K_DOWN,K_LEFT,K_RIGHT],False,0]
    p2=[None,"player2",[K_e,K_d,K_s,K_f],False,0]
    p3=[None,"player3",[K_i,K_k,K_j,K_l],False,0]
    p4=[None,"player4",[K_KP5,K_KP2,K_KP1,K_KP3],False,0]
    #0=tp , 1=nom , 2=keys , 3=bot(0)/human(1) , 4=etape anim perso menu
    bts=[]
    fps=0
    encoure=True
    while encoure:
        t1=time.time()
        #
        if time.time()-dani>=tpan:
            dani=time.time()
            if p1[0]!=None:
                p1[4]+=1
                if p1[4]>=len(animspersos[p1[0]]): p1[4]=0
            if p2[0]!=None:
                p2[4]+=1
                if p2[4]>=len(animspersos[p2[0]]): p2[4]=0
            if p3[0]!=None:
                p3[4]+=1
                if p3[4]>=len(animspersos[p3[0]]): p3[4]=0
            if p4[0]!=None:
                p4[4]+=1
                if p4[4]>=len(animspersos[p4[0]]): p4[4]=0
        #
        bts=aff_menu(p1,p2,p3,p4,fps)
        #
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE: encoure=False
            elif event.type==MOUSEBUTTONDOWN:
                pos=pygame.mouse.get_pos()
                for b in bts:
                    if b != None and b.collidepoint(pos):
                        di=bts.index(b)
                        if di==0: main_jeu(p1,p2,p3,p4)
                        elif di==1:
                            if p1[0]==None: p1[0]=-1
                            else: p1[0]+=1
                            if p1[0]>=len(tpanims): p1[0]=None
                            p1[4]=0
                        elif di==2: p1[3]=not p1[3]
                        elif di==3:
                            if p2[0]==None: p2[0]=-1
                            else: p2[0]+=1
                            if p2[0]>=len(tpanims): p2[0]=None
                            p2[4]=0
                        elif di==4: p2[3]=not p2[3]
                        elif di==5:
                            if p3[0]==None: p3[0]=-1
                            else: p3[0]+=1
                            if p3[0]>=len(tpanims): p3[0]=None
                            p3[4]=0
                        elif di==6: p3[3]=not p3[3]
                        elif di==7:
                            if p4[0]==None: p4[0]=-1
                            else: p4[0]+=1
                            if p4[0]>=len(tpanims): p4[0]=None
                            p4[4]=0
                        elif di==8: p4[3]=not p4[3]
        t2=time.time()
        tt=(t2-t1)
        if tt!=0: fps=int(1./tt)
                        
 
main_menu()



"""
Doodle Man !
A doodle jump clone
Written by Abiye Enzo
08/10/2022 - V1.0
"""
from random import randint
from ion import keydown as kDwn
from time import monotonic as mntnc,sleep
from kandinsky import fill_rect as rect, draw_string as text

xi = input("Une partie de jeu offert par\n\t\t\tBlack-N-Zo\n\n\n\tCliquez pour continuer")
SCREEN_W=320
SCREEN_H=222

GAME_W=200
SCORE_W=100
GAME_H=200

OFFSET_X=(SCREEN_W-SCORE_W-GAME_W)//2
OFFSET_Y=(SCREEN_H-GAME_H)//2

MID_SCREEN=OFFSET_Y+10

KEYS={"L":0,"R":3,"bk":17}

TYPES=["simple","fake","moving","trampo","fantom"]

COLOR={"ddl":(255,50,50),
"eyes":(255,255,255),
"bg":(50,50,50),
"bg2":(70,70,70),
"font1":(200,200,200),
"font2":(255,255,255),
"simple":(255,200,0),
"fake":(70,70,100),
"moving":(50,200,0),
"trampo":(0,150,0),
"fantom":(50,50,255)}

TARG_FPS=30
TARG_FD=1/TARG_FPS#targetted frame during

def s(x):
  """return 's' since 'x'"""
  return mntnc()-x

def drawPauseText():
  txt="GAME PAUSED"
  x=GAME_W//2-len(txt)*5+OFFSET_X
  y=GAME_H//2-10+OFFSET_Y
  text(txt,x,y,COLOR["font2"],COLOR["bg2"])


def drawDll(x,y,s,c):
  rect(int(x),int(y),int(s),int(s),c)
  
  if c!=COLOR["bg"]:
    s_eye=s//4
    x_eye=int(x)+s//2+int(ddl["spd_x"]*ddl["size"]/ddl_init_size)
    c_eyes=COLOR["eyes"]
    
    rect(x_eye-s_eye-1,int(y)+s//2-s_eye//2,int(s_eye),int(s_eye),c_eyes)
    rect(x_eye+1,int(y)+s//2-s_eye//2,int(s_eye),int(s_eye),c_eyes)
  
  
def drawPlatform(x,y,hs,vs,c):
  
  if y>OFFSET_Y+GAME_H-vs:
    vs-=(y-(OFFSET_Y+GAME_H-vs))
  
  if y<=limits["y"][1]:
    rect(int(x),int(y),int(hs),int(vs),c)

def drawPlatforms(mode=None):
  
  x_ddl=ddl_prvs[0]
  y_ddl=ddl_prvs[1]
  s_ddl=ddl["size"]
  
  for p in platforms:
    x=p[0]
    y=p[1]
    hs=p[2]
    vs=p[3]
    t=p[4]
    c=p[5]
    lx=p[6]
    ly=p[7]
        
    if t=="moving":
      drawPlatform(lx,ly,hs,vs,COLOR["bg"])
      for p2 in platforms:
        if hitBox(p2,[lx,ly,hs,vs]) and not p==p2:
          drawPlatform(p2[0],p2[1],p2[2],p2[3],p2[5])
        
    if mode=="all" or t=="moving":
      drawPlatform(x,y,hs,vs,c)
      p[6]=x
      p[7]=y
        
    if hitBox(p,[x_ddl,y_ddl,s_ddl,s_ddl]):
      drawPlatform(x,y,hs,vs,c)
      p[6]=x
      p[7]=y      

def addPlatform(y):
 
  global cf
  
  try: cf==0
  except:cf=0#consecutive fake
  
  while True:
    
    np=createPlatform(y)
    if np!=None:
      if np[4]=="fake":
        if cf==1:
          np[4]="simple"
          np[5]=COLOR["simple"]
          cf=0
        else:cf+=1
      else:
        cf=0
      break
  platforms.append(np)
      
def createPlatform(y):
   
    hs=int(platform_hor_size)-score//2000 #horizontal size
    vs=hs//6 #vertical size
    
    limits_x=[OFFSET_X+5,GAME_W+OFFSET_X-hs-5]
    
    x=randint(limits_x[0],limits_x[1])
  
    t=TYPES[randint(0,len(TYPES)-1)]
    
    rand=randint(0,100)
    if rand<=percentages[t]:
      p=[x,y,hs,vs,t,COLOR[t],x,y,0.5]
      return p
      

def hitBox(p1,p2):
  x1=p1[0]
  y1=p1[1]
  hs1=p1[2]
  vs1=p1[3]
  
  x2=p2[0]
  y2=p2[1]
  hs2=p2[2]
  vs2=p2[3]
  
  if x1 <= x2+hs2 and x1+hs1 >= x2 and y1 <= y2+vs2 and y1+vs1 >= y2:
    return True
  else:
    return False

def game_engine():
  
  global ddl,ddl_prvs,ddl_init_size,limits,platforms,percentages,score,best_score,platform_hor_size,platform_vert_size
  
  ddl_init_size=20
  
  ddl={
  "x":OFFSET_X+GAME_W//2-ddl_init_size//2,
  "y":MID_SCREEN,
  "spd_x":0.0,
  "spd_y":0,
  "size":ddl_init_size,
  "color":COLOR["ddl"]}
  ddl_prvs=[0,0,0,0,(0,0,0)]
  
  print(">init game engine...")
  
  rect(0,0,SCREEN_W,SCREEN_H,COLOR["bg2"])
  
  speed=0.07
  jump_speed=2.4
  
  platform_hor_size=30
  
  score=0
  best_score=readBestScore()

  #init map
  drawScorePannel()
  rect(OFFSET_X,OFFSET_Y,GAME_W,GAME_H,COLOR["bg"])
  
  #limit : x[min][max], y[min][max]
  limits={
  "x":[OFFSET_X,OFFSET_X+GAME_W-ddl["size"]+1],
  "y":[OFFSET_Y,OFFSET_Y+GAME_H]}
    
  #init platforms
  percentages={"simple":50,"fake":40,"moving":40,"trampo":5,"fantom":5}
  
  platforms=[[OFFSET_X,
  limits["y"][1]-5,GAME_W,5,"simple",COLOR["simple"],OFFSET_X,limits["y"][1],0]]
  
  for y in range(OFFSET_Y+60,GAME_H+OFFSET_Y-5,60):
    addPlatform(y)
    
  drawPlatforms("all")
  draw_all=0
  
  draw_timer=mntnc()-TARG_FD
  fps=TARG_FPS
  lpf=1 #lapse_per_frame
  targ_tics=240
  targ_lpf=targ_tics/fps
  spd_corrector=1
  
  print(">launch the game...")
  
  while True:
    if s(draw_timer)>=TARG_FD:
      
      fps=int(1/s(draw_timer))
      targ_lpf=targ_tics//fps
      spd_corrector=lpf/targ_lpf
      lpf=0
      
      if draw_all:
        rect(OFFSET_X,OFFSET_Y,GAME_W,GAME_H,COLOR["bg"])
        drawPlatforms("all")
        draw_all=0
        
      else:
        drawDll(ddl_prvs[0],ddl_prvs[1],ddl_prvs[2],COLOR["bg"])
        drawPlatforms()
      
      if score>=best_score:
        best_score = score
      
      actualizeScore()
      
      drawDll(ddl["x"],ddl["y"],ddl["size"],COLOR["ddl"])
      ddl_prvs=[ddl["x"],ddl["y"],ddl["size"]]
      if kDwn(KEYS["bk"]):
        drawPauseText()
        while kDwn(KEYS["bk"]):
          pass
        while not kDwn(KEYS["bk"]):
          pass
        while kDwn(KEYS["bk"]):
          pass
        draw_all=1
      draw_timer=mntnc()
      
    lpf+=1
    ddl["x"]+=ddl["spd_x"]
    if ddl["y"]<=MID_SCREEN and ddl["spd_y"]<0:
      
      score-=int(ddl["spd_y"]*spd_corrector)//10
      
      for p in platforms:
        if p[1]<=limits["y"][1]-5:
          p[1]-=ddl["spd_y"]
          draw_all=1
        
        else:  
          platforms.remove(p)
          addPlatform(OFFSET_Y)

    else:
      ddl["y"]+=ddl["spd_y"]
    
    if ddl["x"]<limits["x"][0]:
      ddl["x"]=limits["x"][0]
      ddl["spd_x"]=0
    
    if ddl["x"]>limits["x"][1]:
      ddl["x"]=limits["x"][1]
      ddl["spd_x"]=0
    
    if ddl["y"]+ddl["size"]<=limits["y"][0]:
      ddl["y"]-=ddl["spd_y"]
      ddl["spd_y"]=0
    
    if ddl["y"]<=limits["y"][0]:
      ddl["y"]=limits["y"][0]
    
    
    if ddl["y"]+ddl["size"]>=limits["y"][1]:
      ddl["y"]=limits["y"][1]-ddl["size"]
      
      drawDll(ddl_prvs[0],ddl_prvs[1],ddl_prvs[2],COLOR["bg"])
      drawDll(ddl["x"],ddl["y"],ddl["size"],ddl["color"])
      
      print(">game end: dead...")
      print(">fps : {}".format(fps))
      print(">spd_corrector : {}, lpf : {}/{}".format(spd_corrector,lpf,targ_lpf))
      saveScore(best_score)
      deathAnimation()
      break
      
    if kDwn(KEYS["R"]):
      ddl["spd_x"]+=speed*spd_corrector
    
    if kDwn(KEYS["L"]):
      ddl["spd_x"]-=speed*spd_corrector
        
    for p in platforms:
      if hitBox(p,[ddl["x"],ddl["y"]+ddl["size"]-5,ddl["size"],5]) and ddl["spd_y"]>=0:
        
        if p[4]=="trampo":
          ddl["spd_y"]=-jump_speed*2*spd_corrector
        
        elif p[4]=="fantom":
          p[4]="fake"
          p[5]=COLOR["fake"]
          drawPlatform(p[0],p[1],p[2],p[3],p[5])
          ddl["spd_y"]=-jump_speed*spd_corrector
          
        elif p[4]=="fake":
          pass
        
        else:
          ddl["spd_y"]=-jump_speed*spd_corrector
          
        percentages[p[4]]*=0.01
        
      if p[4]=="moving":
          if p[0]<=OFFSET_X+1 or p[0]>=OFFSET_X+GAME_W-p[2]-1:
            p[8]=-p[8]
          p[0]+=p[8]*spd_corrector
          
    
    ddl["spd_x"]/= 1.02
    ddl["spd_y"]+=0.02 * spd_corrector
    
    ddl["size"]=ddl_init_size-score//2000

    limits={
    "x":[OFFSET_X,OFFSET_X+GAME_W-ddl["size"]],
    "y":[OFFSET_Y,OFFSET_Y+GAME_H]}
    
    
def transition():
  for c in [COLOR["font1"],COLOR["bg"]]:
    for y in range(OFFSET_Y,OFFSET_Y+GAME_H,10):
      sleep(0.016)
      rect(OFFSET_X,y,GAME_W,10,c)
  

def actualizeScore():
  
  x=OFFSET_X+GAME_W+SCORE_W//2
  y=OFFSET_Y+score_off
  
  text(str(score),x-len(str(score))*5,y+40,COLOR["font2"],COLOR["bg"])
  
  c=COLOR["simple"] if score==best_score else COLOR["font2"]
  text(str(best_score),x-len(str(best_score))*5,y+100,c,COLOR["bg"])
  
  
def drawScorePannel(): 
  global score_off
  
  x=OFFSET_X+GAME_W
  y=OFFSET_Y
  
  score_off=5
  
  rect(x+score_off,y,SCORE_W-2*score_off,GAME_H,COLOR["font1"])
  rect(x+2*score_off,y+score_off,SCORE_W-4*score_off,GAME_H-2*score_off,COLOR["bg"])
  
  x=OFFSET_X+GAME_W+SCORE_W//2
  y=OFFSET_Y+score_off
  
  text("SCORE",x-len("SCORE")*5,y+10,COLOR["font1"],COLOR["bg"])
  text("BEST",x-len("BEST")*5,y+70,COLOR["font1"],COLOR["bg"])
  
  s=ddl["size"]
  drawDll(x-s//2,y+140,s,COLOR["ddl"])


def deathAnimation():
  transition()
  game_engine()

def readBestScore():
  try:
    file=open("ddl_man.sav","r")
    best = file.readline()
    file.close()
    print(">score loaded !")
    return int(best)
  except:
    print(">failed to read the score...")
    return 0
  
def saveScore(score):
  try :
    file=open("ddl_man.sav","w")
    file.truncate(0)
    file.write(str(score))
    file.close()
    print(">score saved !")
  except:
    print(">failed to save the score...")
    
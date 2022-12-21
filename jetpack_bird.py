from kandinsky import fill_rect as krect, draw_string as text
from ion import keydown
from random import randint
from time import *
# Code by Abiye Enzo
SCREEN_W=320
SCREEN_H=222

GAME_W=200
SCORE_OFFSET=5
SCORE_W=100
GAME_H=200

OFFSET_X=(SCREEN_W-SCORE_W-GAME_W-SCORE_OFFSET)//2# game offset
OFFSET_Y=(SCREEN_H-GAME_H)//2

KEY={"ok":4}
COLOR={
"bg":(50,200,255),
"bird":(255,200,0),
"hurt":(255,50,0),
"jp":(150,150,150),
"mouth":(255,100,0),
"pipe":(100,255,20),
"line":(0,0,0),
"font1":(60,60,60),
"font2":(255,255,255)}

LINE_W=2 #line width

TARG_FPS=20
TARG_SPF=1/TARG_FPS# targ second per frame

def sec(time):
  return monotonic()-time

def rect(x,y,h_s,v_s,c):
  krect(int(x),int(y),int(h_s),int(v_s),COLOR["line"])
  if h_s>2*LINE_W: krect(int(x)+LINE_W,int(y)+LINE_W,int(h_s)-2*LINE_W,int(v_s)-2*LINE_W,c)

def drawBird(x,y,s):
  if sec(hurt_time)>1 or (sec(hurt_time)*5%2>0.5):
    c=COLOR["bird"]
  else:
    c=COLOR["hurt"]
  rect(x,y,s,s,c)
  rect(x-s/2,y+s/8,s/2,s/2,COLOR["jp"])
  rect(x+s/2,y+s/2,s/1.5,s/3,COLOR["mouth"])
  rect(x+s/4,y+s/5,s/3,s/3,COLOR["font2"])  
  
  o=s/2 if flap and int(sec(flap_time)*16)%2==0 else s/4
  rect(x-s/4,y+o,s/2,s/2,c)
  if flap:
    s2=min(s/2+o*2,OFFSET_Y+GAME_H-y-s/8*6)
    rect(x-s/2,y+s/8*5,s/2,s2,COLOR["mouth"])
    krect(int(x-s/2+LINE_W*2),int(y+s/8*5.5),int(s/2-LINE_W*4),int(s2/2),COLOR["font2"])
  
  
def drawPipe(i):
  pipe=pipes[i]
  
  x,y = min(max(pipe[0],OFFSET_X),OFFSET_X+GAME_W),pipe[1]
  if x<=OFFSET_X: h_s = pipe[2]-(x-pipe[0])
  elif x>=OFFSET_X+GAME_W-pipe[2]: h_s = (GAME_W+OFFSET_X)-x
  else: h_s=pipe[2]
  v_s = pipe[3]
  
  rect(x,y,h_s,v_s,COLOR["pipe"])

def drawHeart(x,y,s,c):
  heart=("01100","11110","01111","11110","01100")
  for x2 in range(len(heart)):
    for y2 in range(len(heart[x2])):
      if int(heart[x2][y2]): krect(x+x2*s,y+y2*s,s,s,c)

def initScreen():
  rect(OFFSET_X,OFFSET_Y,GAME_W,GAME_H,COLOR["bg"])
  drawScorePannel()
  actualizeScore()
  actualizeLife()

def clearScreen():
  krect(OFFSET_X+LINE_W,OFFSET_Y+LINE_W,GAME_W-2*LINE_W,GAME_H-2*LINE_W,COLOR["bg"])
  
def createPipe(x,y,h_s,v_s):
  #h_s : horizontal size
  #v_s : vertical size
  pipe=[x,y,h_s,v_s]
  pipes.append(pipe)
  

def addPipes(x,s):
  space_size = GAME_H//2 - difficulty*2
  space_y= randint(OFFSET_Y,OFFSET_Y+GAME_H-space_size-20)
  
  createPipe(x,OFFSET_Y,s,space_y)
  createPipe(x,OFFSET_Y+space_size+space_y,s,GAME_H-(space_size+space_y))
  
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

def gameEngine():
  global bird, pipes, score, best_score, difficulty,flap,total_time,flap_time,fps,hurt_time,life
  
  print(">initialisation: dead...")    
  difficulty=1
  life=3
  score=0
  best_score=readBestScore()
  pipes=[]
  pipe_size=50
  flap=0
  jump_speed=4
  max_speed=15
  fps=TARG_FPS
 
  bird={
  "x":20,
  "y":OFFSET_Y+GAME_H/2,
  "spd_x":5,
  "spd_y":-5,
  "size":20,
  "color":COLOR["bird"]}
  
  addPipes(GAME_W+OFFSET_X,pipe_size)
  addPipes(GAME_W/2-pipe_size/2+OFFSET_X,pipe_size)
  
  initScreen()
  
  spf=TARG_SPF
  total_time=monotonic()
  flap_time=monotonic()
  hurt_time=monotonic()-1
  
  while not (life<1 and sec(hurt_time)>0.5):
    if sec(spf)>=TARG_SPF:
      
      #GAME DATA
      fps=int(1/sec(spf))
      #print(fps)
      spf=monotonic()
      
      #PHYSICS
      limits_y=[OFFSET_Y,OFFSET_Y+GAME_H]
      
      bird["spd_y"]+=jump_speed/3
      bird["spd_y"]=max(-max_speed,min(max_speed,bird["spd_y"]))
      
      bird["y"]+=bird["spd_y"]
      
      if bird["y"]<=limits_y[0]:
        bird["y"]=limits_y[0]
        bird["spd_y"]=0
      
      if bird["y"]>=limits_y[1]-bird["size"]:
        bird["y"]=limits_y[1]-bird["size"]
        bird["spd_y"]=0
        
      if keydown(KEY["ok"]):
        bird["spd_y"]-=abs(-max_speed-bird["spd_y"])/max_speed*jump_speed
        if flap==0:
          flap_time=monotonic()
        flap=1
      else: flap=0
      
      remove_pipe=[]
      last_speed=int(bird["spd_x"])
      for i in pipes:
        i[0]-=last_speed
        if hitBox((bird["x"],bird["y"],bird["size"],bird["size"]),i):
          if sec(hurt_time)>1:
            if life>0:hurt_time=monotonic()
            life-=1
            difficulty+=randint(1,3)
            actualizeLife()
            print(">{}s:hurt! life:{}".format(int(sec(total_time)),life))
        if i[0]+i[2]<=OFFSET_X:
          if i[1]!=OFFSET_Y:
            bird["spd_x"]+=abs(max_speed-bird["spd_x"])/(4*max_speed)
            score+=1
            best_score=max(score,best_score)
            actualizeScore()
            addPipes(GAME_W+OFFSET_X,pipe_size)
          remove_pipe.append(i)
      for i in remove_pipe:
        pipes.remove(i)
                
      #DISPLAY
      clearScreen()
      for i in range(len(pipes)):
        drawPipe(i)
      drawBird(bird["x"],bird["y"],bird["size"])
    
  print(">game end: dead...")
  print(">fps : {}".format(fps))
  transition()
  saveScore(best_score)
  gameEngine()
      
def actualizeScore():
  
  x=OFFSET_X+GAME_W+SCORE_OFFSET+SCORE_W//2
  y=OFFSET_Y
  c=COLOR["font2"]
  
  text(str(score),x-len(str(score))*5,y+40,c,COLOR["bird"])
  text(str(best_score),x-len(str(best_score))*5,y+100,c,COLOR["bird"])
  
def actualizeLife():
  
  x=OFFSET_X+GAME_W+SCORE_OFFSET+5
  y=OFFSET_Y+150
  
  for i in range(3):
    if i>=life: c=COLOR["line"]
    else: c=COLOR["hurt"]
    drawHeart(x+i*30,y,5,c) 

def drawScorePannel(): 

  x=OFFSET_X+GAME_W+SCORE_OFFSET
  y=OFFSET_Y
  
  rect(x,y,SCORE_W,GAME_H,COLOR["bird"])
  
  x=OFFSET_X+GAME_W+SCORE_W//2
  y=OFFSET_Y
  
  text("SCORE",x-len("SCORE")*5,y+10,COLOR["font1"],COLOR["bird"])
  text("BEST",x-len("BEST")*5,y+70,COLOR["font1"],COLOR["bird"])
  
def readBestScore():
  try:
    file=open("jp_bird.sav","r")
    best = file.readline()
    file.close()
    print(">score loaded !")
    return int(best)
  except:
    print(">failed to read the score...")
    return 0

def saveScore(score):
  try :
    file=open("jp_bird.sav","w")
    file.truncate(0)
    file.write(str(score))
    file.close()
    print(">score saved !")
  except:
    print(">failed to save the score...")

def transition():
  for c in [COLOR["font1"],COLOR["bg"]]:
    for y in range(OFFSET_Y,OFFSET_Y+GAME_H,10):
      sleep(0.016)
      krect(OFFSET_X,y,GAME_W,10,c)

gameEngine()